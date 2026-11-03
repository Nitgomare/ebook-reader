(function(){
 'use strict';
 const app=document.querySelector('.app'),svg=app.querySelector('svg'),panel=app.querySelector('.panel');
 const stage=document.createElement('div');stage.className='figure-stage';stage.setAttribute('aria-label','动画显示区域');svg.before(stage);stage.append(svg);
 const controls=document.createElement('section');controls.className='figure-position-controls';controls.innerHTML='<h2>整体平移</h2><label>水平平移 <output id="figure-pan-x-value">0%</output><input id="figure-pan-x" type="range" min="-100" max="100" step="1" value="0" aria-label="整体水平平移"></label><label>垂直平移 <output id="figure-pan-y-value">0%</output><input id="figure-pan-y" type="range" min="-100" max="100" step="1" value="0" aria-label="整体垂直平移"></label><button id="figure-center" type="button">平移归零</button><p>平移只改变取景位置。参数变化保持同一缩放比例；滚轮可手动缩放。</p>';panel.append(controls);
 let panX=0,panY=0,redraw=()=>{};const fits=new WeakMap();
 function offsets(){const v=svg.viewBox.baseVal;return {x:panX/100*v.width*.7,y:panY/100*v.height*.7}}
 function sync(){document.getElementById('figure-pan-x').value=panX;document.getElementById('figure-pan-y').value=panY;document.getElementById('figure-pan-x-value').textContent=panX+'%';document.getElementById('figure-pan-y-value').textContent=panY+'%'}
 ['x','y'].forEach(axis=>document.getElementById('figure-pan-'+axis).addEventListener('input',e=>{if(axis==='x')panX=Number(e.target.value);else panY=Number(e.target.value);sync();redraw()}));
 function resetPan(){panX=panY=0;sync();redraw()}
 document.getElementById('figure-center').onclick=resetPan;
 window.FigureLayout={
  offsets,
  fit(scene,state,span){const W=Math.max(240,Math.round(svg.clientWidth)),H=Math.max(240,Math.round(svg.clientHeight)),key=W+':'+H;let entry=fits.get(scene);svg.setAttribute('viewBox',`0 0 ${W} ${H}`);svg.setAttribute('preserveAspectRatio','xMidYMid meet');if(!entry||entry.key!==key){const ratio=entry?scene.state.scale/entry.initial:1;const initial=Math.min(W*.78/span,H*.74/span);scene.state.scale=initial*ratio;scene.defaults.scale=initial;entry={key,initial};fits.set(scene,entry);scene.baseOrigin.x=W*.5;scene.baseOrigin.y=H*.57;scene.origin.x=scene.baseOrigin.x;scene.origin.y=scene.baseOrigin.y}if(state){state.compact=W<500;if('scale' in state)state.scale=scene.state.scale}},
  attach(scene,state,render,span){redraw=render;const project=scene.project.bind(scene);scene.project=function(v){const p=project(v),o=offsets();return {...p,x:p.x+o.x,y:p.y+o.y}};this.fit(scene,state,span);const observer=new ResizeObserver(()=>{this.fit(scene,state,span);render()});observer.observe(stage);window.figureView={get scale(){return scene.state.scale},project:v=>scene.project(v),get pan(){return {x:panX,y:panY}}};render()},
  attachSimple(state,origin,render,span){redraw=render;const adapter={state,defaults:{scale:state.scale},baseOrigin:{...origin},origin};this.fit(adapter,null,span);new ResizeObserver(()=>{this.fit(adapter,null,span);render()}).observe(stage);window.figureView={get scale(){return state.scale},get pan(){return {x:panX,y:panY}}};render()}
 };
 svg.addEventListener('dblclick',()=>{panX=panY=0;sync();redraw()});
 panel.querySelectorAll('#reset,.reset').forEach(button=>button.addEventListener('click',resetPan));
 let lastHeight=0;
 const reportHeight=()=>{const height=Math.ceil(app.getBoundingClientRect().height);if(height!==lastHeight){lastHeight=height;parent.postMessage({type:'textbook:figure-height',height},'*')}};
 new ResizeObserver(reportHeight).observe(app);window.addEventListener('load',reportHeight);
}());
