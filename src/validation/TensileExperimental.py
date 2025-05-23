from validation.experimental import full_experiment
from validation.get_vector import get_vector
import matplotlib.pyplot as plt

def TensileExperimental():

    df = full_experiment()
    df = df[["Name","Modulo (GPa)","Espesor (mm)",r"% epsilon","Tension maxima Traccion (MPa)"]]

    df_stats = df.groupby('Name').agg(['mean', 'std'])

    composition = [
            ["Y"],
            ["Y", "X"],
            ["Y", "SX"],
            ["Y", "SY"],
            ["Y","SX", "SY"],
            ["Y","X", "SY"]
        ]
    df_stats["layers"] = composition
    
    
    df_stats['v [X,SX,Y,SY]'] = df_stats['layers'].apply(get_vector)
    df_stats["ni"] = df_stats["layers"].apply(len)

    # cambiar de nombre Modulo (GPa) -> E[GPa]
    df_stats.rename(columns={"Modulo (GPa)": "Et [GPa]",
                             "Espesor (mm)": "t [mm]",
                            r"% epsilon": r"% e",
                            "Tension maxima Traccion (MPa)": "St [MPa]" 
                             }, 
                    inplace=True)
    return {
        "df": df,
        "df_stats": df_stats
    }


def TensilePlotData(df_stats):

    # plot bars with error bars Espesor (mm)
    fig = plt.figure(figsize=(9, 4))
    ax = fig.add_subplot(121)
    df_stats['t [mm]'].plot(kind='bar', y='mean', 
                            yerr='std', 
                            legend=False, 
                            title='Espesor (mm)', 
                            ax=ax)
    # ticks angle
    plt.xticks(rotation=45)
    plt.xlabel('') 

    # plot bars with error bars Modulo Tracción [MPa]
    plt.grid()
    ax = fig.add_subplot(122)
    df_stats['Et [GPa]'].plot(kind='bar', y='mean', yerr='std', legend=False, title='Modulo Tracción [GPa]', ax=ax)
    plt.grid()
    # off xlabel
    plt.xlabel('') 
    plt.xticks(rotation=45)