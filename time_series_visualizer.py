import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv(
    "./fcc-forum-pageviews.csv",
    index_col='date',
    parse_dates=True
)

# Clean data
df = df[
    (df['value'] >= df['value'].quantile(0.025))
    & (df['value'] <= df['value'].quantile(1.0-0.025))
]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(12,4), layout='constrained')

    ax.plot(
        df.index.to_numpy(dtype='datetime64[D]'),
        df.values,
        color='r',
    )

    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    df_bar['Years'] = df_bar.index.year
    df_bar['Months'] = df_bar.index.month

    df_bar = df_bar.groupby(['Years', 'Months']).mean()
    df_bar = df_bar.unstack()

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(6,6), layout='constrained')

    df_bar.plot(kind="bar", ax=ax)

    month_names = pd.to_datetime([i for i in range(1,13)], format='%m').month_name()

    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.legend(title="Months", labels=month_names)

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    #Result of strftime depends on locale, this is more portable:
    df_box['month'] = df_box.date.dt.month_name().str.slice(stop=3)

    month_ord = pd.to_datetime([i for i in range(1,13)], format='%m').month_name().str.slice(stop=3)

    # Draw box plots (using Seaborn)
    fig, axs = plt.subplots(
        ncols=2,
        figsize=(18,6),
        layout='constrained'
    )

    sns.boxplot(
        data=df_box,
        ax=axs[0],
        x='year',
        y='value',
        hue='year',
        palette='colorblind',
        legend=False
    )

    axs[0].set_title('Year-wise Box Plot (Trend)')
    axs[0].set_xlabel('Year')
    axs[0].set_ylabel('Page Views')
    axs[0].set_ylim(0, 200000)
    axs[0].set_yticks([20000*i for i in range(0,11)])

    sns.boxplot(
        data=df_box,
        ax=axs[1],
        x='month',
        order=month_ord,
        y='value',
        hue='month',
        palette='muted',
        legend=False
    )

    axs[1].set_title('Month-wise Box Plot (Seasonality)')
    axs[1].set_xlabel('Month')
    axs[1].set_ylabel('Page Views')
    axs[1].set_ylim(0, 200000)
    axs[1].set_yticks([20000*i for i in range(0,11)])

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
