const T=Viz3D.THREE, TAU=Math.PI*2, clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)), smooth=x=>{x=clamp(x);return x*x*(3-2*x)};
const canvas=document.getElementById("stage"), renderer=new T.WebGLRenderer({canvas,antialias:false});
renderer.setPixelRatio(1);renderer.outputColorSpace=T.SRGBColorSpace;renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=1.05;
const scene=new T.Scene();scene.background=new T.Color("#000104");
const camera=new T.PerspectiveCamera(36,9/16,.1,100);
scene.add(new T.HemisphereLight(0xb4dfff,0x111124,2.1));
for(const [x,y,z,c,p] of [[-4,5,6,0xffffff,12],[4,1,3,0xffba58,9],[-2,-4,4,0x33bfff,8]]){
 const l=new T.PointLight(c,p);l.position.set(x,y,z);scene.add(l);
}
const steel=new T.MeshStandardMaterial({color:0x8fabbc,metalness:.85,roughness:.34});
const brass=new T.MeshStandardMaterial({color:0xd8a338,metalness:.88,roughness:.23});
const black=new T.MeshStandardMaterial({color:0x101c2b,metalness:.65,roughness:.45});
const ruby=new T.MeshStandardMaterial({color:0xef4444,emissive:0xef4444,emissiveIntensity:.25,metalness:.3,roughness:.16});
const cyan=new T.MeshStandardMaterial({color:0x67e8f9,emissive:0x22d3ee,emissiveIntensity:.4,metalness:.7,roughness:.3});
const white=new T.MeshStandardMaterial({color:0xe4f5ff,emissive:0x4e899a,emissiveIntensity:.22,metalness:.65,roughness:.25});

const envScene=new T.Scene();envScene.background=new T.Color(0x526278);
for(const [x,y,z,w,h,c] of [[0,0,5,7,3,0xe5f5ff],[4,0,0,4,8,0xffca84],[-4,0,0,3,7,0x8cbcff],[0,-5,1,6,3,0xffffff]]){
 const panel=new T.Mesh(new T.PlaneGeometry(w,h),new T.MeshBasicMaterial({color:c,side:T.DoubleSide}));panel.position.set(x,y,z);panel.lookAt(0,0,0);envScene.add(panel);
}
const pmrem=new T.PMREMGenerator(renderer);scene.environment=pmrem.fromScene(envScene,.12).texture;pmrem.dispose();

const root=new T.Group();scene.add(root);
function mesh(g,m,parent=root){const o=new T.Mesh(g,m);parent.add(o);return o}
function cyl(r,h,m,parent=root){const o=mesh(new T.CylinderGeometry(r,r,h,64),m,parent);o.rotation.x=Math.PI/2;return o}
function ring(r,t,m,parent=root){return mesh(new T.TorusGeometry(r,t,8,96),m,parent)}
function bar(a,b,w,m,parent=root){const d=new T.Vector3().subVectors(b,a);const o=mesh(new T.BoxGeometry(w,w,d.length()),m,parent);o.position.copy(a).add(b).multiplyScalar(.5);o.quaternion.setFromUnitVectors(new T.Vector3(0,0,1),d.normalize());return o}
function screw(x,y,z,parent=root){const o=cyl(.075,.055,steel,parent);o.position.set(x,y,z);const slot=mesh(new T.BoxGeometry(.105,.018,.01),black,parent);slot.position.set(x,y,z+.032)}
const movementSteel=new T.MeshStandardMaterial({color:0x304553,metalness:.82,roughness:.48});
const plate=cyl(3,.16,movementSteel);plate.position.z=-.18;ring(3,.08,steel).position.z=-.10;
for(let i=0;i<60;i++){const a=i*TAU/60;const o=mesh(new T.BoxGeometry(.024,i%5?.07:.16,.035),i%5?steel:brass);o.position.set(2.83*Math.cos(a),2.83*Math.sin(a),.015);o.rotation.z=a+Math.PI/2}
function gear(x,y,r,n,z){const g=new T.Group();g.position.set(x,y,z);root.add(g);ring(r*.78,r*.12,brass,g);ring(r*.26,r*.08,steel,g);
 for(let i=0;i<n;i++){const a=i*TAU/n,o=mesh((n===15?new T.CylinderGeometry(r*.10,r*.055,.12,3):new T.BoxGeometry(r*.18,r*.16,.12)),brass,g);o.position.set(r*Math.cos(a),r*Math.sin(a),0);o.rotation.z=a}
 for(let i=0;i<5;i++){const a=i*TAU/5;bar(new T.Vector3(0,0,0),new T.Vector3(r*.74*Math.cos(a),r*.74*Math.sin(a),0),r*.085,brass,g)}
 cyl(.085,.045,ruby,g).position.z=.09;return g;
}
for(const [x,y,r] of [[-1.25,.95,.93],[.1,.95,.6],[.93,.47,.5],[.85,-.45,.67],[-.70,-1.34,.91]]){const recess=cyl(r,.055,black);recess.position.set(x,y,-.025);ring(r,.013,steel).position.set(x,y,.01);}
const gears=[gear(-1.25,.95,.85,40,.12),gear(.10,.95,.52,28,.20),gear(.93,.47,.42,22,.26)];
const barrel=new T.Group();root.add(barrel);barrel.position.set(-1.25,.95,.30);ring(.68,.045,steel,barrel);
function spiral(turns,inner,outer,z){const pts=[];for(let i=0;i<=480;i++){const u=i/480,a=u*turns*TAU,r=inner+(outer-inner)*u;pts.push(new T.Vector3(Math.cos(a)*r,Math.sin(a)*r,z))}
 return new T.TubeGeometry(new T.CatmullRomCurve3(pts),480,.014,5,false)}
const spring=mesh(spiral(6,.08,.61,.03),cyan,barrel);
spring.geometry.morphAttributes.position=[spiral(.7,.08,.67,.03).attributes.position];spring.updateMorphTargets();
const escape=gear(.85,-.45,.59,15,.42);
const fork=new T.Group();fork.position.set(.72,-1.43,.54);root.add(fork);
const pivot=new T.Vector3(0,0,0),ends=[new T.Vector3(-.40,.70,0),new T.Vector3(.59,.72,0)];
for(const p of ends)bar(pivot,p,.095,steel,fork);
bar(pivot,new T.Vector3(-.1,-.42,0),.08,brass,fork);cyl(.11,.12,ruby,fork);
const pallets=ends.map((p,i)=>{const o=mesh(new T.BoxGeometry(.17,.18,.16),ruby,fork);o.position.copy(p);o.rotation.z=i?-.3:.3;return o});
const balance=new T.Group();balance.position.set(-.70,-1.34,.63);root.add(balance);
ring(.82,.065,brass,balance);ring(.71,.015,steel,balance);
for(let i=0;i<3;i++){const a=i*TAU/3;bar(new T.Vector3(),new T.Vector3(.78*Math.cos(a),.78*Math.sin(a),0),.07,brass,balance)}
for(let i=0;i<12;i++){const a=i*TAU/12;const o=cyl(.052,.095,steel,balance);o.position.set(.81*Math.cos(a),.81*Math.sin(a),0)}
const hairGroup=new T.Group();hairGroup.position.copy(balance.position);hairGroup.position.z+=.12;root.add(hairGroup);mesh(spiral(5,.07,.60,0),cyan,hairGroup);
cyl(.075,.08,ruby,balance).position.z=.1;
for(const [x,y] of [[-1.25,.95],[.10,.95],[.93,.47],[.85,-.45],[-.7,-1.34],[.72,-1.43]]){
 const j=ring(.125,.022,steel);j.position.set(x,y,.5);
}
for(const [x,y] of [[-2.1,1.8],[1.8,1.8],[-2.2,-1.7],[1.7,-1.9]])screw(x,y,.1);
for(const [a,b] of [[[-2.1,1.8,.37],[-.3,1.8,.37]],[[1.8,1.8,.48],[1.8,-.2,.48]]]){bar(new T.Vector3(...a),new T.Vector3(...b),.20,steel);for(const p of [a,b])screw(...p)}
for(let i=0;i<24;i++){const a=i*TAU/24;const o=ring(2.65+i*.004,.0025,steel);o.position.z=-.08;}
for(const [x,y] of [[.24,-1.35],[1.2,-1.4]]){const p=cyl(.045,.25,steel);p.position.set(x,y,.57)}
const ghosts=gears.concat([escape]).map(g=>{const o=g.clone();o.traverse(c=>{if(c.isMesh){c.material=c.material.clone();c.material.transparent=true;c.material.opacity=.16;c.material.depthWrite=false}});root.add(o);return o});
const sparkMat=new T.MeshStandardMaterial({color:0xffef93,emissive:0xffb52f,emissiveIntensity:1.5});
const spark=mesh(new T.IcosahedronGeometry(.07,0),sparkMat);
const dial=new T.Group();root.add(dial);dial.position.set(0,0,1);
ring(2.50,.028,steel,dial);dial.visible=false;
for(let i=0;i<12;i++){const a=i*TAU/12;const o=mesh(new T.BoxGeometry(.055,.19,.06),white,dial);o.position.set(Math.sin(a)*2.4,Math.cos(a)*2.4,0);o.rotation.z=-a}
function hand(l,w,m,z){const group=new T.Group();dial.add(group);const o=mesh(new T.BoxGeometry(w,l,.045),m,group);o.position.set(0,l*.42,z);return group}
const hands=[hand(2.25,.032,ruby,.12),hand(1.75,.075,white,.07),hand(1.2,.11,brass,.03)];cyl(.13,.13,ruby,dial).position.z=.14;
const hudCanvas=document.createElement('canvas');hudCanvas.width=768;hudCanvas.height=260;const hc=hudCanvas.getContext('2d');
const hudTex=new T.CanvasTexture(hudCanvas);hudTex.magFilter=T.NearestFilter;hudTex.minFilter=T.NearestFilter;
const hud=new T.Mesh(new T.PlaneGeometry(4.2,1.42),new T.MeshBasicMaterial({map:hudTex,transparent:true,depthTest:false}));hud.renderOrder=20;scene.add(hud);
const target=new T.WebGLRenderTarget(360,640,{minFilter:T.NearestFilter,magFilter:T.NearestFilter});
const postScene=new T.Scene(),postCam=new T.OrthographicCamera(-1,1,1,-1,0,1);
const postMat=new T.ShaderMaterial({uniforms:{image:{value:target.texture}},vertexShader:'varying vec2 uv0;void main(){uv0=uv;gl_Position=vec4(position.xy,0.,1.);}',fragmentShader:'uniform sampler2D image;varying vec2 uv0;void main(){vec4 c=texture2D(image,uv0);vec3 a=c.rgb*1.6;vec3 rgb=pow(clamp((a*(2.51*a+.03))/(a*(2.43*a+.59)+.14),0.,1.),vec3(1./2.2));gl_FragColor=vec4(floor(rgb*31.+.5)/31.,1.);}'});
postScene.add(new T.Mesh(new T.PlaneGeometry(2,2),postMat));
let width=1080,height=1920;
const stage={safeBox(){return {x:width*.07,y:height>width?height*.15:height*.07,width:width*.86,height:height>width?height*.62:height*.86}},resize(w,h){width=w;height=h;renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();target.setSize(Math.round(w/3),Math.round(h/3));}};
function sim(t){if(t<16.5)return t;if(t<25)return 16.5+(t-16.5)/50;if(t<33){const u=t-25;return 16.67+u*.5+u*u/32}return 22.67+t-33}
function state(t){const s=sim(t),p=s*8,n=Math.floor(p),u=p-n,step=smooth(u/.18);
 const chaos=t>=6&&t<10.5,unwind=smooth((t-6)/.6),rew=smooth((t-10.5)/1);
 return {s,p,n,u,step,chaos,extra:t<6?0:t<10.5?unwind*TAU*12:(1-rew)*TAU*12,
 lift:t<6?0:t<10.5?smooth((t-6)/.25)*3.5:(1-rew)*3.5,
 rate:t<16.5?8:t<25?.16:t<33?8*(.5+(t-25)/16):8};}
const shots=[
[0,[-.2,.1,.2],8.7],[3,[-.8,.6,.3],7.5],[6,[0,0,.2],8.7],[8.5,[-.7,.6,.4],7],
[11.5,[.72,-.8,.5],4.3],[14,[.85,-.65,.5],3.8],[16.5,[.85,-.75,.5],3.15],[19.5,[.8,-.8,.5],2.85],[22.5,[.72,-.9,.5],3.2],
[25,[-.7,-1.34,.6],3.7],[28,[-.7,-1.34,.6],3.2],[30.5,[-.7,-1.34,.6],3.8],[33,[0,0,.3],8.8],[36,[0,0,.3],8.2],[39.5,[0,0,.3],8.5]];
function seek(t){t=clamp(t,0,42);const st=state(t);
 gears.forEach((g,i)=>g.rotation.z=(st.n+st.step)*TAU/[480,-144,64][i]+st.extra*(i%2?-1:1)*(i+1));
 escape.rotation.z=-(st.n+st.step)*TAU/15+st.extra*4;
 ghosts.forEach((g,i)=>{const source=[...gears,escape][i];g.visible=st.chaos;g.position.copy(source.position);g.rotation.z=source.rotation.z+.04+.1*Math.sin(t*90+i)});
 fork.position.z=.54+st.lift;fork.rotation.z=.10*Math.cos(st.s*TAU*4);
 balance.rotation.z=.95*Math.sin(st.s*TAU*4);const breath=1+.075*Math.sin(st.s*TAU*4);hairGroup.scale.set(breath,breath,1);hairGroup.rotation.z=.12*Math.sin(st.s*TAU*4);
 spring.rotation.z=st.extra;spring.morphTargetInfluences[0]=clamp(st.extra/(TAU*12));spring.scale.setScalar(1+st.extra/(TAU*12)*.85);
 spark.visible=st.u<.20&&!st.chaos;spark.position.set(.85+(st.n%2?-.39:.30),-.78,.69);spark.scale.setScalar(.35+.8*(1-clamp(st.u/.20)));
 dial.visible=t>=33;dial.scale.setScalar(smooth((t-33)/1.6));hands[0].rotation.z=-Math.floor(st.s*8)/8*TAU/60;hands[1].rotation.z=-.7-st.s*TAU/3600;hands[2].rotation.z=1.0-st.s*TAU/43200;
 let i=shots.length-1;while(i>0&&shots[i][0]>t)i--;const a=shots[i],prev=shots[Math.max(0,i-1)],mix=smooth((t-a[0])/.65),focus=new T.Vector3(...prev[1]).lerp(new T.Vector3(...a[1]),mix);
 let distance=(prev[2]+(a[2]-prev[2])*mix)*(1+.035*Math.sin((t-a[0])*Math.PI/1.5));distance*=camera.aspect>1?1.00:1.75;
 if(a[2]>7){const safe=stage.safeBox();distance=Math.max(distance,3.12/(Math.tan(T.MathUtils.degToRad(camera.fov/2))*camera.aspect*(safe.width/width)));}
 const az=.24+Math.sin(t*.36)*.12;camera.position.copy(focus).add(new T.Vector3(Math.sin(az)*distance,-distance*.43,distance*.90));
 if(st.chaos){camera.position.x+=.045*Math.sin(t*137);camera.position.y+=.04*Math.cos(t*113)}
 camera.lookAt(focus);camera.updateMatrixWorld();
 hc.clearRect(0,0,768,260);hc.fillStyle='#081221';hc.fillRect(0,0,768,260);hc.fillStyle='#64e9ff';hc.font='bold 25px monospace';
 const rows=[['FREQ (VPH)','28,800'],['TICKS/SEC',st.chaos?'FREE':st.rate.toFixed(st.rate<1?2:1)],['SPRING %',String(Math.round(t<6?100:t<10.5?100*(1-smooth((t-6)/.6)):100*smooth((t-10.5))))],['TIME SCALE',t>=16.5&&t<25?'50x SLOW':st.chaos?'UNLOCKED':t>=25&&t<33?(8/st.rate).toFixed(1)+'x SLOW':'1x']];
 rows.forEach((r,i)=>{const x=i%2*380+24,y=Math.floor(i/2)*110+42;hc.fillStyle='#7d99ac';hc.fillText(r[0],x,y);hc.fillStyle='#e0f8ff';hc.font='bold 35px monospace';hc.fillText(r[1],x,y+42);hc.font='bold 25px monospace'});
 hudTex.needsUpdate=true;hud.quaternion.copy(camera.quaternion);
 const hudDistance=6,hsize=2*Math.tan(T.MathUtils.degToRad(camera.fov/2))*hudDistance;
 hud.position.copy(camera.position).add(new T.Vector3(0,-hsize*(camera.aspect<1?.23:.34),-hudDistance).applyQuaternion(camera.quaternion));hud.scale.setScalar(Math.min(hsize*camera.aspect*.86/4.2,hsize*(camera.aspect<1?.14:.19)/1.42));
 renderer.setRenderTarget(target);renderer.render(scene,camera);renderer.setRenderTarget(null);renderer.render(postScene,postCam);
 window.watchState={...st,safeBox:stage.safeBox(),t};
}
window.watch={state,sim,shots};window.OPENER={ready:true,resize:stage.resize,seek};stage.resize(1080,1920);seek(0);
