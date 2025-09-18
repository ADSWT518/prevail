#!/usr/bin/python3
# Usage: python3 makeplot.py results.csv [loads|stores|instructions|...] [showTrendline]
import matplotlib.pyplot as plt
import numpy as np
import sys

if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
    print('Usage: {} FILE.csv [key] [showTrendline]')
    print('For example:')
    print('    python3 {} results.csv iterations False'.format(sys.argv[0]))
    sys.exit(64)

data = np.genfromtxt(sys.argv[1], delimiter=',', names=True)

key = 'stores' if len(sys.argv) < 3 else sys.argv[2]
trendline = True if len(sys.argv) < 4 else (sys.argv[3] == "True")


def plot_and_save(title, field, units, suffix, filename):
    fig = plt.figure(figsize=(3, 2.8))  # 设置图的大小为 8x6
    sp = fig.add_subplot(111)
    sp.set_title(title)
    sp.set_xlabel(field)
    sp.set_ylabel(units)
    field_data = data[field]
    space = np.linspace(min(field_data), max(field_data), 2)
    for label in data.dtype.fields:
        if not label.endswith(suffix): continue
        deg = 1
        arr = data[label]
        color = next(plt.gca()._get_lines.prop_cycler)['color']
        if trendline:
            sp.plot(space, np.poly1d(np.polyfit(field_data, arr, deg))(space), color=color)
        sp.plot(field_data, arr, color=color, label=label,
                        marker='.',
                        markerfacecolor='None',
                        linestyle = 'None')
    sp.legend()
    plt.tight_layout()  # 调整子图布局
    plt.savefig(filename, format='pdf')


plot_and_save("", 'instructions', '', '_sec', 'sec_vs_{}.pdf'.format(key))
plot_and_save("", 'instructions', '', '_gb', 'memory_vs_{}.pdf'.format(key))