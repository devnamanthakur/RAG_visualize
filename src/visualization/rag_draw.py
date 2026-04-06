import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

def draw_rag(processes , allocated_matrix, need_matrix , total_resources):
    fig, ax=plt.subplots(figsize=(14,8))
    ax.set_xlim(0,12)
    ax.set_ylim(0,10)
    ax.axis("off")

    n_proc=len(processes)
    n_res=len(total_resources)

    y_vals_proc=np.linspace(9,1,n_proc)
    proc_pos={p:(1.5,y_vals_proc[i])for i,p in enumerate(processes)}

    res_names=[f"R{j}" for j in range(1,n_res+1)]
    y_vals_res = np.linspace(9,1,n_res)
    res_pos= dict(zip(res_names,[(6,y)for y in y_vals_res]))

    for p,(x,y) in proc_pos.items():
        circle =mpatches.Circle(
            (x,y),0.45,color="#d4f1d4" , ec="black",lw=1.5,zorder=3
        )
        ax.add_patch(circle)
        ax.text(
            x,y,p,ha="center",va="center",
            fontsize=10,fontweight="bold",zorder=4
        )


    Max_dots=4

    for j,r in enumerate(res_names):
            x,y = res_pos[r]
            resct =mpatches.FancyBboxPatch(
                (x-0,55,y-0.4),1.1,0.8,
                boxstyle="round,pad=0.05",
                color="#1a7a4a" , ec="black" ,lw=1.5,zorder=3
            )

            ax.add_patch(rect)
            ax.text(
                x,y+0.65,r,
                ha="center", va="center",
                fontsize=10,fontweight="bold",zorder=4
            )

            count=total_resources[j]
            if count<=Max_dots:
                x_positions=np.linspace(-0.25,0.25,count)
                for dx in x_positions:
                    ax.plot(
                        x+dx,y,"o",
                        color="white", markersize=7 , zorder=5
                    )

            else:
                ax.text(
                    x,y,str(count),
                    ha="center",va="center", 
                    color="white",fontsize=11,fontweight="bold",zorder=5
                )
    
    arrow_kw=dict(arrowstyle="->",lw=1.8, coonectionstyle="arc3,rad=0.1")

    for i,p in enumerate(processes):
        px,py=proc_pos[p]
        for j in range(n_res):
             rx,ry=res_pos[f"R{j+1}"]

             if allocated_matrix[i][j]>0:
                  ax.annotate(
                    "", xy=(px + 0.45, py), xytext=(rx - 0.55, ry),
                    arrowprops={**arrow_kw, "color": "#2563eb"},
                    zorder=2,
                )
             if need_matrix[i][j]>0:
                   ax.annotate(
                    "", xy=(rx - 0.55, ry), xytext=(px + 0.45, py),
                    arrowprops={
                        **arrow_kw,
                        "color": "#dc2626",
                        "linestyle": "dashed",
                    },
                    zorder=2,
                )

    legends_handles=[
         mpatches.Patch(color="#2563eb", label="Assignment (R->P)"),
         mpatches.Patch(color="#dc2626",label="Request(P->R)"),
    ]
    ax.legend(handles=legend_handles,loc="lower right",fontsize=10)
    ax.set_title("Resource Allocation Graph", fontsize=14,fontweight="bold")       

    return fig
                


   