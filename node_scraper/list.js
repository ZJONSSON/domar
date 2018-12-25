const Promise = require('bluebird');
const request = require('request');
const requestAsync = Promise.promisify(request);
const cheerio = require('cheerio');
const etl = require('etl');

const search = {
  searchaction: 'Search',
  pageid: 'deb3ce16-7d66-11e5-80c6-005056bc6a40',
  verdict: '',
  court: '',
  casenumber: '',
  lawparagraphs: '',
  parties: '',
  fromdate: '',
  todate: '01.01.2020'
};

const courts = [
  {url: 'https://www.heradsdomstolar.is/'},
  {url: 'https://www.haestirettur.is/', court: 'Hæstiréttur'},
  {url: 'https://www.landsrettur.is/', court: 'Landsréttur'}
];

let total = 0;

module.exports = argv => etl.toStream(courts)
  .pipe(etl.map(5, async function(data) {
    if (argv.court && !data.url.includes(argv.court)) return;
    const res = await requestAsync({
      url: data.url,
      qs: search,
      gzip: true,
      proxy: argv.getProxy(),
      timeout: 10000
    });

    const count = +/Leitin skilaði (\d+)/.exec(res.body)[1];

    total += count;
    
    for (let i = 0; i < count; i+= 100) {
      this.push(Object.assign({offset:i, count: 100}, data));
    }

  }))
  .pipe(etl.map(argv.concurrency || 30, async function(data) {

    const qs = Object.assign({
      offset: data.offset,
      count: data.count,
      SortBy:''
    },search);

    const res = await requestAsync({
      url: data.url,
      qs,
      gzip: true,
      proxy: argv.getProxy(),
      timeout: 10000
    });

    const $ = cheerio.load(res.body);

    $('.result').map( (i,v) => this.push({
      url: data.url+$(v).find('a').attr('href'),
      case: $(v).find('h2').text(),
      date: $(v).find('time').attr('datetime'),
      court: data.court || $(v).find('h3').text(),
      clerk: $(v).find('.person').text(),
      abstract: $(v).find('.case-abstract').text(),
      offset: qs.offset,
      __total: total
    }));
  
  }, {
    catch: function(e,d) {
      console.log('retry',e);
      this.write(d);
    }
  }));