define(["./when-4bbc8319","./Transforms-f15de320","./Matrix2-c6c16658","./RuntimeError-5b082e8f","./ComponentDatatype-3d0a0aac","./GeometryAttribute-8350368e","./GeometryAttributes-7827a6c2","./combine-e9466e32","./WebGLConstants-508b9636"],(function(e,t,n,r,i,a,o,c,u){"use strict";function s(){this._workerName="createPlaneOutlineGeometry"}s.packedLength=0,s.pack=function(e,t){return t},s.unpack=function(t,n,r){return e.defined(r)?r:new s};const y=new n.Cartesian3(-.5,-.5,0),m=new n.Cartesian3(.5,.5,0);return s.createGeometry=function(){const e=new o.GeometryAttributes,r=new Uint16Array(8),c=new Float64Array(12);return c[0]=y.x,c[1]=y.y,c[2]=y.z,c[3]=m.x,c[4]=y.y,c[5]=y.z,c[6]=m.x,c[7]=m.y,c[8]=y.z,c[9]=y.x,c[10]=m.y,c[11]=y.z,e.position=new a.GeometryAttribute({componentDatatype:i.ComponentDatatype.DOUBLE,componentsPerAttribute:3,values:c}),r[0]=0,r[1]=1,r[2]=1,r[3]=2,r[4]=2,r[5]=3,r[6]=3,r[7]=0,new a.Geometry({attributes:e,indices:r,primitiveType:a.PrimitiveType.LINES,boundingSphere:new t.BoundingSphere(n.Cartesian3.ZERO,Math.sqrt(2))})},function(t,n){return e.defined(n)&&(t=s.unpack(t,n)),s.createGeometry(t)}}));