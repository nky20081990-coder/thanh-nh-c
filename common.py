
import numpy as np
import plotly.graph_objects as go
from math import pi

def box(center, size, color, name, opacity=0.92):
    cx,cy,cz = center
    dx,dy,dz = np.array(size)/2
    x=[cx-dx,cx+dx,cx+dx,cx-dx,cx-dx,cx+dx,cx+dx,cx-dx]
    y=[cy-dy,cy-dy,cy+dy,cy+dy,cy-dy,cy-dy,cy+dy,cy+dy]
    z=[cz-dz,cz-dz,cz-dz,cz-dz,cz+dz,cz+dz,cz+dz,cz+dz]
    i=[0,0,4,4,0,1,2,3,0,3,1,2]
    j=[1,2,5,6,4,5,6,7,3,7,2,6]
    k=[2,3,6,7,5,1,7,4,4,4,5,5]
    return go.Mesh3d(x=x,y=y,z=z,i=i,j=j,k=k,color=color,opacity=opacity,
                     name=name,hovertemplate=f"<b>{name}</b><extra></extra>")

def cylinder(center, radius, height, color, name, axis="Y", opacity=0.95, n=32):
    cx,cy,cz=center
    t=np.linspace(0,2*pi,n)
    if axis=="Y":
        x1=cx+radius*np.cos(t); z1=cz+radius*np.sin(t); y1=np.full(n,cy-height/2)
        x2=cx+radius*np.cos(t); z2=cz+radius*np.sin(t); y2=np.full(n,cy+height/2)
    elif axis=="X":
        y1=cy+radius*np.cos(t); z1=cz+radius*np.sin(t); x1=np.full(n,cx-height/2)
        y2=cy+radius*np.cos(t); z2=cz+radius*np.sin(t); x2=np.full(n,cx+height/2)
    else:
        x1=cx+radius*np.cos(t); y1=cy+radius*np.sin(t); z1=np.full(n,cz-height/2)
        x2=cx+radius*np.cos(t); y2=cy+radius*np.sin(t); z2=np.full(n,cz+height/2)
    x=np.r_[x1,x2]; y=np.r_[y1,y2]; z=np.r_[z1,z2]
    ii=[];jj=[];kk=[]
    for q in range(n-1):
        ii += [q,q+n]; jj += [q+1,q+1+n]; kk += [q+n,q+1]
    ii += [n-1,2*n-1]; jj += [0,n]; kk += [n,0]
    for q in range(1,n-1):
        ii.append(0); jj.append(q+1); kk.append(q)
        ii.append(n); jj.append(n+q); kk.append(n+q+1)
    return go.Mesh3d(x=x,y=y,z=z,i=ii,j=jj,k=kk,color=color,opacity=opacity,
                     name=name,hovertemplate=f"<b>{name}</b><extra></extra>")

def gear(center, outer, root, width, color, name, teeth=12, axis="Y"):
    # Simplified engineering gear: alternating outer/root radial profile.
    cx,cy,cz=center
    angles=np.linspace(0,2*pi,teeth*2,endpoint=False)
    radii=np.array([outer if i%2==0 else root for i in range(teeth*2)])
    if axis=="Y":
        x=cx+radii*np.cos(angles); z=cz+radii*np.sin(angles)
        y0=np.full(len(x),cy-width/2); y1=np.full(len(x),cy+width/2)
        xb=np.r_[x,x]; yb=np.r_[y0,y1]; zb=np.r_[z,z]
    else:
        y=cy+radii*np.cos(angles); z=cz+radii*np.sin(angles)
        x0=np.full(len(y),cx-width/2); x1=np.full(len(y),cx+width/2)
        xb=np.r_[x,x]; yb=np.r_[y,y]; zb=np.r_[z,z]
    N=len(x)
    ii=[];jj=[];kk=[]
    for q in range(N):
        q2=(q+1)%N
        ii += [q,q]; jj += [q2,q2+N]; kk += [q+N,q+N]
    # front/back faces
    center0=N*2
    xb=np.r_[xb, cx]; yb=np.r_[yb, cy] ; zb=np.r_[zb, cz]
    # Simpler side-only mesh plus center fan
    return go.Mesh3d(x=xb[:2*N],y=yb[:2*N],z=zb[:2*N],i=ii,j=jj,k=kk,
                     color=color,opacity=.96,name=name,
                     hovertemplate=f"<b>{name}</b><extra></extra>")

def shaft(points, color, name, width=7):
    p=np.array(points)
    return go.Scatter3d(x=p[:,0],y=p[:,1],z=p[:,2],mode="lines",
                        line=dict(color=color,width=width),name=name,
                        hovertemplate=f"<b>{name}</b><extra></extra>")

def setup_fig(fig, xr, yr, zr, camera=None, height=720):
    fig.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)", height=height,
        margin=dict(l=0,r=0,t=5,b=0), showlegend=False,
        scene=dict(
            xaxis=dict(title="X — chiều ngang",range=xr,zeroline=False),
            yaxis=dict(title="Y — chiều dọc",range=yr,zeroline=False),
            zaxis=dict(title="Z — chiều cao",range=zr,zeroline=False),
            aspectmode="manual", aspectratio=dict(x=1,y=1.25,z=.78),
            camera=camera or dict(eye=dict(x=1.7,y=1.8,z=1.25))
        )
    )
    return fig
