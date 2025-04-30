from matplotlib import pyplot as plt
import numpy as np

def plot_E(df_stats, E_eff_exp, E_eff_pred, Evec_opt, En_opt):
    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_subplot(211)
    offset = 0.15
    # bar plot tau_exp and tau_pred in the same plot separated by a gap
    xspan = range(len(df_stats.index))
    # ax.bar([x-offset for x in xspan], tau_exp, width=offset, label='Experimental')
    try:
        error = df_stats['Et [GPa]']['std'].values
    except:
        error = df_stats['Eb [GPa]']['std'].values
    
    ax.bar([x-offset for x in xspan], E_eff_exp, yerr=error, width=offset, label='Experimental', capsize=5)
    ax.bar([x+offset for x in xspan], E_eff_pred, width=offset, label='Predicción')
    ax.set_xticks(xspan);
    ax.set_xticklabels(df_stats.index);
    ax.legend()
    # t [mm]
    plt.ylabel('Modulo Flexión [GPa]')
    plt.grid()

    # print in plot the values of optimal tn and tl
    fz = 11
    fd = {'color':'black','weight':'bold',"family":'serif'}
    # in title
    Evec_opt_str = "  ,  ".join([f"{E:.2f}" for E in Evec_opt])
    # E_vec[0],E_vec[1],E_vec[2],E_vec[3] = E_l_X,E_l_Y,E_l_SX,E_l_SY

    names = [r"{X}",r"{SX}",r"{Y}",r"{SY}"]
    title_str = "  ,  ".join([f"$E_{names[i]}$ = {Evec_opt[i]:.2f}" for i in range(4)])
    plt.title(f' $E_n = {En_opt:.2f} \\ $ |  {title_str}', fontsize=fz)

    ax = fig.add_subplot(212)
    # relative error
    error = 100*abs(E_eff_exp - E_eff_pred)/E_eff_exp
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
    plt.ylim(0,20)

