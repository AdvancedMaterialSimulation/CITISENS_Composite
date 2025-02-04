# bar plot compare tau_exp and tau_pred
from matplotlib import pyplot as plt
def plt_thin(df_stats, tau_exp, tau_pred, tn_opt, tl_opt):
    fig = plt.figure(figsize=(9, 4))
    ax = fig.add_subplot(211)
    offset = 0.15
    # bar plot tau_exp and tau_pred in the same plot separated by a gap
    xspan = range(len(df_stats.index))
    # ax.bar([x-offset for x in xspan], tau_exp, width=offset, label='Experimental')
    error = df_stats['Espesor (mm)']['std'].values
    ax.bar([x-offset for x in xspan], tau_exp, yerr=error, width=offset, label='Experimental', capsize=5)
    ax.bar([x+offset for x in xspan], tau_pred, width=offset, label='Predicted')
    ax.set_xticks(xspan);
    ax.set_xticklabels(df_stats.index);
    ax.legend()
    # t [mm]
    plt.ylabel('Espesor (mm)')
    plt.grid()

    # print in plot the values of optimal tn and tl
    fz = 12
    fd = {'color':'black','weight':'bold',"family":'serif'}
    # in title 
    plt.title(f' $t_n = {tn_opt:.2f} \\ [mm]$ |  $t_l ={tl_opt:.2f} \\ [mm]$', fontsize=fz,fontdict=fd)

    ax = fig.add_subplot(212)
    # relative error
    error = 100*abs(tau_exp - tau_pred)/tau_exp
    ax.bar(xspan, error, width=0.4)
    # ylabel
    plt.ylabel('Error relativo (%)')
    # horizontal line at 5%
    plt.axhline(5, color='r', linestyle='--',label='5%')
    plt.grid()
    # mean error horizontal line
    mean_error = error.mean()
    plt.axhline(mean_error, color='g', linestyle='--',label='Error medio = {:.2f}%'.format(mean_error))
    ax.set_xticks(xspan);
    ax.set_xticklabels(df_stats.index);
    ax.legend()

    plt.ylim(0, 20)
