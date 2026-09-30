const http=require('node:http'),fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..'),source=path.join(root,'content/books/robot-technology-basics/docs/interactive'),built=path.join(root,'dist/files/robot-technology-basics/interactive');
(async()=>{
 const denied=[];
 const server=http.createServer((req,res)=>{
  const u=new URL(req.url,'http://localhost');
  if(u.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(`<html><body style="margin:0"><iframe style="width:100%;height:100vh;border:0" sandbox="allow-scripts" src="${u.searchParams.get('frame')}"></iframe></body></html>`);return}
  if(!req.headers.cookie?.includes('figure_test=ok')){denied.push(u.pathname);res.statusCode=401;res.end('Authentication required');return}
  const folder=u.pathname.startsWith('/source/')?source:built,file=path.join(folder,path.basename(u.pathname));
  if(!fs.existsSync(file)){res.statusCode=404;res.end();return}
  res.setHeader('Content-Type',file.endsWith('.js')?'application/javascript':file.endsWith('.css')?'text/css':'text/html');res.end(fs.readFileSync(file));
 });await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const origin='http://127.0.0.1:'+server.address().port;
 const browser=await chromium.launch({headless:true,...(process.env.CHROMIUM_PATH?{executablePath:process.env.CHROMIUM_PATH}:{})});const context=await browser.newContext();await context.addCookies([{name:'figure_test',value:'ok',url:origin,sameSite:'Lax'}]);const page=await context.newPage();
 await page.goto(origin+'/?frame=/source/figure-3-9.html');await page.waitForTimeout(300);
 assert.ok(denied.some(u=>u.endsWith('.js')),'original failure must reproduce: authenticated script is blocked in opaque sandbox');console.log('REPRODUCED: original external helper rejected inside authenticated sandbox');denied.length=0;
 const errors=[];page.on('pageerror',e=>errors.push(e.message));let count=0;
 for(const width of [1000,390]){await page.setViewportSize({width,height:900});for(const file of fs.readdirSync(built).filter(f=>f.endsWith('.html'))){await page.goto(origin+'/?frame=/built/'+file);const frame=page.frames().find(f=>f!==page.mainFrame());await frame.waitForFunction(()=>!!window.figureView);const result=await frame.evaluate(()=>{const s=document.querySelector('.figure-stage').getBoundingClientRect();const overlap=[...document.querySelectorAll('.panel,.readout,.hint')].some(e=>{const r=e.getBoundingClientRect();return r.left<s.right&&r.right>s.left&&r.top<s.bottom&&r.bottom>s.top});return {overlap,lines:document.querySelectorAll('svg line,svg polyline').length,controls:!!document.querySelector('#figure-pan-x')}});assert.equal(result.overlap,false);assert.ok(result.lines>0);assert.equal(result.controls,true);count++;if(file==='figure-3-9.html')await page.screenshot({path:process.env.TEMP+'/authenticated-figure-'+width+'.png',fullPage:false})}}
 assert.deepEqual(denied,[]);assert.deepEqual(errors,[]);console.log('PASS:',count,'authenticated sandbox renders; no blocked resources, blank animations or panel overlap');await browser.close();await new Promise(resolve=>server.close(resolve));
})().catch(e=>{console.error(e);process.exit(1)});
