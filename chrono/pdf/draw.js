/* ============ PR-01 · planta da tampa ============ */
(function(){
  const host=document.getElementById("pl-plan");
  const bb=p=>{let a=1e9,b=-1e9,c=1e9,d=-1e9;for(const q of p){a=Math.min(a,q[0]);b=Math.max(b,q[0]);c=Math.min(c,q[1]);d=Math.max(d,q[1]);}
    return Math.max(b-a,d-c);};
  const small=ps=>ps.filter(p=>bb(p)<60), big=ps=>ps.filter(p=>bb(p)>=60);
  const s=el("svg",{viewBox:"-74 -104 208 214"});
  s.style.width="107mm"; s.style.margin="0 auto";
  const g=el("g",{transform:"scale(1,-1)"});
  g.appendChild(el("path",{d:pathOf(big(GEO.plan.painel)),fill:"none",stroke:"var(--hair)","stroke-width":.4}));
  g.appendChild(el("path",{d:pathOf(big(GEO.plan.furo)),fill:"none",stroke:"var(--hair)","stroke-width":.4}));
  g.appendChild(el("path",{d:pathOf(GEO.plan.aro),fill:"none",stroke:"var(--pc-tampa)","stroke-width":.7}));
  g.appendChild(el("path",{d:pathOf(small(GEO.plan.painel)),fill:"none",stroke:"var(--ink)","stroke-width":.5}));
  g.appendChild(el("path",{d:pathOf(small(GEO.plan.furo)),fill:"none",stroke:"var(--signal)","stroke-width":.6}));
  g.appendChild(el("circle",{cx:0,cy:12.18,r:4.06,fill:"none",stroke:"var(--signal)","stroke-width":.5,"stroke-dasharray":"1.6 1.1"}));
  g.appendChild(el("circle",{cx:0,cy:-4.96,r:.89,fill:"none",stroke:"var(--signal)","stroke-width":.4}));
  s.appendChild(g);
  const ln=(x1,y1,x2,y2,c="var(--faint)",w=.32,d=null)=>{
    const a={x1,y1,x2,y2,stroke:c,"stroke-width":w}; if(d)a["stroke-dasharray"]=d; s.appendChild(el("line",a));};
  const tx=(x,y,t,anc="middle",col="var(--muted)",sz=4.6)=>{
    const n=el("text",{x,y,"text-anchor":anc,fill:col,"font-size":sz,"font-family":"IBM Plex Mono, monospace"});
    n.textContent=t; s.appendChild(n);};
  ln(-61.1,97,61.1,97); ln(-61.1,94.5,-61.1,99.5); ln(61.1,94.5,61.1,99.5); tx(0,104,"122,15");
  ln(-68,-92.5,-68,92.5); ln(-70.5,-92.5,-65.5,-92.5); ln(-70.5,92.5,-65.5,92.5);
  const r=el("text",{fill:"var(--muted)","font-size":4.6,"text-anchor":"middle",
    "font-family":"IBM Plex Mono, monospace",transform:"translate(-70.5,0) rotate(-90)"});
  r.textContent="185,07"; s.appendChild(r);
  tx(0,-97,"12 h","middle","var(--faint)",4.2);
  const call=(y,tag,sub,col,fx,fy)=>{ ln(fx,fy,66,y-1.6,col,.3,"1.8 1.4");
    tx(68,y,tag,"start",col,4.6); tx(68,y+5.6,sub,"start","var(--faint)",3.8); };
  call(-56,"respiro Ø8,12","a 12,18 do centro, a 12 h","var(--signal)",3.4,-14.7);
  call(-26,"rasgo da orelha","abre para Ø44,62, a 3 h e 9 h","var(--signal)",22.4,-3.4);
  call(4,"poço Ø38,54","furo reto de 4,85 mm","var(--signal)",19.3,0);
  call(34,"rebaixo Ø50,05","aba plana, sobe 0,60 mm","var(--pc-tampa)",25.0,5.0);
  call(64,"ponto de injeção Ø1,78","a 4,96 do centro, a 6 h","var(--signal)",0.9,5.9);
  host.appendChild(s);
})();

/* ============ PR-02 · corte ============ */
(function(){
  const host=document.getElementById("pl-sec");
  const X0=-23.5, X1=39.5, Y0=30.0, Y1=43.4;
  const s=el("svg",{viewBox:`${X0} ${-Y1} ${X1-X0} ${Y1-Y0}`});
  s.style.width="170mm";
  const LV=[[32.15,"32,15  fundo do poço"],[35.20,"35,20  topo do ressalto"],
            [37.23,"37,23  face de topo do pino"],[38.24,"38,24  plano de rótulo"],
            [39.72,"39,72  aro de empilhamento"]];
  const g=el("g",{transform:"scale(1,-1)"});
  LV.forEach(([y])=>g.appendChild(el("line",{x1:X0+.4,y1:y,x2:23.0,y2:y,stroke:"var(--grid)","stroke-width":.06})));
  g.appendChild(el("line",{x1:0,y1:30.3,x2:0,y2:42.3,stroke:"var(--grid)","stroke-width":.06,"stroke-dasharray":".6 .5"}));
  g.appendChild(el("path",{d:pathOf(GEO.sec.valv,false),fill:"none",stroke:"var(--pc-pino)","stroke-width":.1,"stroke-dasharray":".7 .45"}));
  g.appendChild(el("path",{d:pathOf(GEO.sec.tampa,false),fill:"none",stroke:"var(--pc-tampa)","stroke-width":.18}));
  const poly=(pts,fill)=>g.appendChild(el("path",{d:"M"+pts.map(p=>p[0]+" "+p[1]).join("L")+"Z",
    fill,stroke:"var(--sheet)","stroke-width":.06}));
  const mir=(pts,fill)=>{poly(pts,fill);poly(pts.map(p=>[-p[0],p[1]]),fill);};
  poly([[-6.3,37.23],[-6.3,38.20],[6.3,38.20],[6.3,37.23]],"var(--pc-pino)");
  mir([[12.2,37.23],[12.2,38.20],[14.2,38.20],[14.2,37.23]],"var(--pc-pino)");
  mir([[6.0,37.25],[6.0,38.18],[12.1,38.18],[12.1,37.25]],"var(--pc-mes)");
  mir([[14.3,37.25],[14.3,38.18],[20.5,38.18],[20.5,37.25]],"var(--pc-dia)");
  s.appendChild(g);
  const F=1.0;
  const tx=(x,y,t,anc="middle",col="var(--muted)",sz=F)=>{
    const n=el("text",{x,y:-y,"text-anchor":anc,fill:col,"font-size":sz,"font-family":"IBM Plex Mono, monospace"});
    n.textContent=t; s.appendChild(n);};
  const lead=(a,b,c,d,col)=>s.appendChild(el("line",{x1:a,y1:-b,x2:c,y2:-d,stroke:col,"stroke-width":.08}));
  const OFF={"37.23":-.85,"38.24":.30};
  LV.forEach(([y,t])=>{ const o=OFF[y.toFixed(2)]||0;
    tx(23.8,y-.33+o,t,"start","var(--faint)",F);
    if(o) s.appendChild(el("line",{x1:23.5,y1:-(y+o),x2:23.0,y2:-y,stroke:"var(--grid)","stroke-width":.06}));
  });
  tx(-15.8,42.8,"casca = válvula atual","middle","var(--pc-pino)");
  lead(-15.8,42.4,-15.8,39.1,"var(--pc-pino)"); lead(-15.8,39.1,-15.2,37.15,"var(--pc-pino)");
  tx(9.25,41.2,"anel de mês Ø24,2/Ø12,0","middle","var(--pc-mes)");
  lead(9.25,40.8,9.25,38.3,"var(--pc-mes)");
  tx(17.4,42.8,"anel de dia Ø41,0/Ø28,6","middle","var(--pc-dia)");
  lead(17.4,42.4,17.4,38.3,"var(--pc-dia)");
  tx(-13.2,32.6,"colar Ø24,4/Ø28,4","middle","var(--pc-pino)");
  lead(-13.2,33.0,-13.2,37.15,"var(--pc-pino)");
  tx(0,35.6,"cubo Ø11,6","middle","var(--pc-pino)"); lead(0,36.0,0,37.15,"var(--pc-pino)");
  tx(7.0,32.4,"respiro Ø8,12","middle","var(--pc-tampa)");
  lead(7.6,32.8,11.6,35.15,"var(--pc-tampa)");
  tx(18.6,31.0,"rasgo da orelha","middle","var(--pc-tampa)");
  lead(18.6,31.4,21.2,35.5,"var(--pc-tampa)");
  host.appendChild(s);
})();

/* ============ PR-03 · datador, estático em 31/08 ============ */
(function(){
  const host=document.getElementById("pl-dial");
  const R=27.5, SD=360/31, SM=30, DIA=31, MES=8;
  const s=el("svg",{viewBox:`${-R} ${-R} ${2*R} ${2*R}`});
  s.style.width="116mm"; s.style.margin="0 auto";
  const flip=el("g",{transform:"scale(1,-1)"}); s.appendChild(flip);
  flip.appendChild(el("circle",{r:25.03,fill:"var(--sunk)",stroke:"var(--pc-tampa)","stroke-width":.18}));
  flip.appendChild(el("circle",{r:24.24,fill:"none",stroke:"var(--pc-tampa)","stroke-width":.1}));
  flip.appendChild(el("circle",{r:19.27,fill:"none",stroke:"var(--pc-tampa)","stroke-width":.2}));
  [1,-1].forEach(sg=>flip.appendChild(el("rect",{x:sg>0?19.0:-22.1,y:-3.2,width:3.1,height:6.4,fill:"var(--pc-pino)"})));

  const rDia=el("g",{transform:`rotate(${-(DIA-1)*SD})`});
  rDia.appendChild(el("path",{d:annulus(20.5,14.3),fill:"var(--pc-dia)","fill-rule":"evenodd"}));
  for(let i=0;i<24;i++){ const a=i*Math.PI/12;
    rDia.appendChild(el("line",{x1:19.55*Math.cos(a),y1:19.55*Math.sin(a),
      x2:20.5*Math.cos(a),y2:20.5*Math.sin(a),stroke:"var(--sheet)","stroke-width":.45})); }
  for(let d=1;d<=31;d++){
    const gg=el("g",{transform:`rotate(${-90+(d-1)*SD}) translate(17.4,0) rotate(90)`});
    const t=el("text",{x:0,y:0,"text-anchor":"middle","dominant-baseline":"central",fill:"var(--sheet)",
      "font-size":2.55,"font-weight":600,"font-family":"IBM Plex Mono, monospace"});
    t.textContent=String(d).padStart(2,"0"); gg.appendChild(t); rDia.appendChild(gg); }
  s.appendChild(rDia);

  const rMes=el("g",{transform:`rotate(${-(MES-1)*SM})`});
  rMes.appendChild(el("path",{d:annulus(12.1,6.0),fill:"var(--pc-mes)","fill-rule":"evenodd"}));
  for(let m=0;m<12;m++){ const a=(-90+m*SM-15)*Math.PI/180;
    rMes.appendChild(el("line",{x1:6.2*Math.cos(a),y1:6.2*Math.sin(a),
      x2:11.9*Math.cos(a),y2:11.9*Math.sin(a),stroke:"var(--sheet)","stroke-width":.32})); }
  for(let m=1;m<=12;m++){
    const gg=el("g",{transform:`rotate(${-90+(m-1)*SM}) translate(9.05,0) rotate(90)`});
    const t=el("text",{x:0,y:0,"text-anchor":"middle","dominant-baseline":"central",fill:"var(--sheet)",
      "font-size":3.05,"font-weight":600,"font-family":"IBM Plex Mono, monospace"});
    t.textContent=String(m).padStart(2,"0"); gg.appendChild(t); rMes.appendChild(gg); }
  s.appendChild(rMes);

  const fix=el("g");
  fix.appendChild(el("path",{d:annulus(14.2,12.2),fill:"var(--pc-pino)","fill-rule":"evenodd",
    stroke:"var(--sheet)","stroke-width":.12}));
  fix.appendChild(el("circle",{r:5.8,fill:"var(--pc-pino)",stroke:"var(--sheet)","stroke-width":.12}));
  const w=16*Math.PI/180;
  fix.appendChild(el("path",{d:`M ${(14.2*Math.sin(-w)).toFixed(3)} ${(-14.2*Math.cos(w)).toFixed(3)}`+
    ` A 14.2 14.2 0 0 1 ${(14.2*Math.sin(w)).toFixed(3)} ${(-14.2*Math.cos(w)).toFixed(3)}`+
    ` L ${(12.2*Math.sin(w)).toFixed(3)} ${(-12.2*Math.cos(w)).toFixed(3)}`+
    ` A 12.2 12.2 0 0 0 ${(12.2*Math.sin(-w)).toFixed(3)} ${(-12.2*Math.cos(w)).toFixed(3)} Z`,
    fill:"var(--signal)"}));
  fix.appendChild(el("path",{d:"M 0 -12.35 L -1.0 -13.15 L 1.0 -13.15 Z",fill:"var(--sheet)"}));
  fix.appendChild(el("path",{d:"M 0 -14.05 L -1.0 -13.25 L 1.0 -13.25 Z",fill:"var(--sheet)"}));
  s.appendChild(fix);

  const extra=el("g",{transform:"scale(1,-1)"});
  extra.appendChild(el("circle",{cx:0,cy:12.18,r:4.06,fill:"none",stroke:"var(--sheet)","stroke-width":.75}));
  extra.appendChild(el("circle",{cx:0,cy:12.18,r:4.06,fill:"none",stroke:"var(--signal)","stroke-width":.34,"stroke-dasharray":"1.2 .9"}));
  extra.appendChild(el("circle",{cx:0,cy:-4.96,r:.89,fill:"none",stroke:"var(--sheet)","stroke-width":.7}));
  extra.appendChild(el("circle",{cx:0,cy:-4.96,r:.89,fill:"none",stroke:"var(--signal)","stroke-width":.32}));
  [1,-1].forEach(sg=>extra.appendChild(el("path",{
    d:`M ${sg*19.27} -3.7 L ${sg*22.31} -3.7 L ${sg*22.31} 3.7 L ${sg*19.27} 3.7`,
    fill:"none",stroke:"var(--signal)","stroke-width":.3,"stroke-dasharray":"1.2 .9"})));
  s.appendChild(extra);

  const lg=el("g");
  lg.appendChild(el("line",{x1:0,y1:-20.9,x2:0,y2:-25.4,stroke:"var(--signal)","stroke-width":.24}));
  const lbl=el("text",{x:1.3,y:-23.2,fill:"var(--signal)","font-size":2.1,"font-family":"IBM Plex Mono, monospace"});
  lbl.textContent="12 h  ·  leitura"; lg.appendChild(lbl);
  s.appendChild(lg);
  host.appendChild(s);
})();
