
#Librerie e moduli importati-------------------------------------------------------------------------------------------------------------------------------------------
import sys
from pathlib import Path
import resources.resources

import PyQt5.QtGui as QG
import PyQt5.QtWidgets as QW

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt import NavigationToolbar2QT as NavTbar
from matplotlib.legend import Legend
import ternary


# Constants--------------------------------------------------------------------
FOIDS = [
    "Nepheline", "Leucite", "Kalsilite", "Analcime", "Sodalite", "Nosean",
    "Hauyne", "Cancrinite", "Pseudo-leucite"
]

GABBRO_MINERALS = ['Olivine', 'Orthopyroxene', 'Clinopyroxene', 'Hornblende']

ULTRAMAFIC_MINERALS = GABBRO_MINERALS + ['Spinel', 'Garnet']

MINERAL_ABBREVIATIONS = {
    'Clinopyroxene': 'CPX',
    'Garnet': 'GRT',
    'Hornblende': 'HBL',
    'Olivine': 'OL',
    'Orthopyroxene': 'OPX',
    'Spinel': 'SP',
}

ICONS_DIR = Path(':') / 'icons' # using QResources

#FUNZIONI PER IL PLOTTING DEI DIAGRAMMI----------------------------------------------(ternary-matplotlib)--------------------------------------------------------------

def PQA_plot(ax, gridon, tickson):

    # Generate figure
    fig, tax = ternary.figure(ax=ax, scale=100)

    # Draw Boundary and Gridlines
    tax.boundary(linewidth=2.0)
    if gridon:
        tax.gridlines(color="black", multiple=5, linewidth=0.5)

    # Set ticks
    if tickson:
        tax.ticks(multiple=10, axis='lbr', linewidth=1, offset=0.015, fontsize=7)

    # Set corners labels
    corners = (('Q', 0.5, 1.01), ('A', 0, 0), ('P', 1, 0))
    for (cname, X, Y) in corners:
        ax.text(X, Y, cname, fontsize=13,
                ha='center', va='bottom',
                transform=tax.get_axes().transAxes)

    # Draw lines
    horiz_lines = (5, 20, 60, 90)
    for hl in (horiz_lines):
        tax.horizontal_line(hl, color='black')

    lines_ends = (((10,0,90), (4,60,36)),                                       # P ratio = 10
                  ((35,0,65), (28,20,52)),                                      # P ratio = 35 (straight part of the line)
                  ((65,0,35), (26,60,14)),                                      # P ratio = 65
                  ((90,0,10), (36,60,4)))                                       # P ratio = 90
    for le in lines_ends:
        tax.line(le[0], le[1], color='black')

    tax.line((28,20,52), (14,60,26),                                            # P ratio = 35 (dotted part of the line)
             color='black', linestyle="--", linewidth=0.5)

    # Plotting fields numbers
    symbols = (('01', (2.5,95,2.5)),      ('02', (12.5,75,12.5)),
               ('03', (3,40,57)),         ('04', (13,40,47)),
               ('05', (30,40,30)),        ('06', (47,40,13)),
               ('07', (57,40,3)),         ('08', (3.5,12.5,84)),
               ('09', (18.5,12.5,69)),    ('10', (43.75,12.5,43.75)),
               ('11', (68.5,12.5,19)),    ('12', (83.5,12.5,4)),
               ('13', (4.5,2.5,93)),      ('14', (21,2.5,76.5)),
               ('15', (48.75,2.5,48.75)), ('16', (76.5,2.5,21)),
               ('17', (93,2.5,4.5)))

    fieldNames = ('quartzolite', 'qtz-rich granitoid', 'alk-feld granite',
                  'syeno-granite', 'monzo-granite', 'granodiorite', 'tonalite',
                  'qtz alk-feld syenite', 'qtz syenite', 'qtz monzonite',
                  'qtz monzodiorite\nqtz monzogabbro',
                  'qtz diorite\nqtz gabbro\nqtz anorthosite',
                  'alk-feld syenite', 'syenite', 'monzonite',
                  'monzodiorite\nmonzogabbro',
                  'diorite\ngabbro\nanorthosite')

    for (sym, pos), name in zip(symbols, fieldNames):
        tax.plot([pos], color='black', marker='${}$'.format(sym),
                     markersize=8, label=name, linestyle='None')

    # Show fields legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[:10], labels[:10], loc='upper left',                      # First column
              bbox_to_anchor=(0, 1.05), framealpha=0, fontsize=7)

    leg2 = Legend(ax, handles[10:], labels[10:], loc = 'upper right',           # Second column
                  bbox_to_anchor=(1, 1.05), framealpha=0, fontsize=7)
    ax.add_artist(leg2)

    return fig, tax


def PFA_plot(ax, gridon, tickson):

    # Generate figure
    fig, tax = ternary.figure(ax=ax, scale=100)

    # Draw Boundary and Gridlines
    tax.boundary(linewidth=2.0)
    if gridon:
        tax.gridlines(color="black", multiple=5, linewidth=0.5)

    # Set ticks
    if tickson:
        tax.ticks(multiple=10, linewidth=1, offset=0.015, fontsize=7)

    # Set Axis labels
    corners = (('F', 0.5, 1.01), ('A', 0, 0), ('P', 1, 0))
    for (cname, X, Y) in corners:
        ax.text(X, Y, cname, fontsize=13,
                ha='center', va='bottom',
                transform=tax.get_axes().transAxes)

    # Draw lines
    tax.horizontal_line(10, color='black')
    tax.horizontal_line(60, color='black')

    lines_ends = (((10,0,90), (4,60,36)),                                       # P ratio = 10
                  ((35,0,65), (63/2.,10,117/2.)),                               # P ratio = 35
                  ((45,10,45), (20,60,20)),                                     # P ratio = 50
                  ((65,0,35), (117/2.,10,63/2.)),                               # P ratio = 65
                  ((90,0,10), (36,60,4)))                                       # P ratio = 90
    for le in lines_ends:
        tax.line(le[0], le[1], color='black')

    # Plotting fields numbers
    symbols = (('01', (10,80,10)),     ('02', (2.5,35,62.5)),
               ('03', (19.5,35,45.5)), ('04', (45.5,35,19.5)),
               ('05', (62.5,35,2.5)),  ('06', (4.5,5,90.5)),
               ('07', (21,5,74)),      ('08', (47.5,5,47.5)),
               ('09', (74,5,21)),      ('10', (91,5,4)))

    fieldNames = ('foidolite', 'foid syenite', 'foid monzosyenite',
                  'foid monzodiorite\nfoid monzogabbro',
                  'foid diorite\nfoid gabbro', 'foid-bearing\nalk-feld syenite',
                  'foid-bear. syenite', 'foid-bear. monzonite',
                  'foid-bear. monzodiorite\nfoid-bear. monzogabbro',
                  'foid-bear. diorite\nfoid-bear. gabbro\nfoid-bear. anorthosite')

    for (sym, pos), name in zip(symbols, fieldNames):
        tax.plot([pos], color='black', marker='${}$'.format(sym),
                     markersize=8, label=name, linestyle='None')


    # Show fields legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[:5], labels[:5], loc='upper left',                        # First column
              bbox_to_anchor=(0, 1.05), framealpha=0, fontsize=7)

    leg2 = Legend(ax, handles[5:], labels[5:], loc = 'upper right',             # Second column
                  bbox_to_anchor=(1, 1.05), framealpha=0, fontsize=7)
    ax.add_artist(leg2)

    return fig, tax


def HblOlPx_plot(ax, gridon, tickson):

    # Generate figure
    fig, tax = ternary.figure(ax=ax, scale=100)

    # Draw Boundary and Gridlines
    tax.boundary(linewidth=2.0)
    if gridon:
        tax.gridlines(color="black", multiple=5, linewidth=0.5)

    # Set ticks
    if tickson:
        tax.ticks(multiple=10, axis='lbr', linewidth=1, offset=0.015, fontsize=7)

    # Set corners labels
    corners = (('Ol', 0.5, 1.01), ('Px', 0, 0), ('Hbl', 1, 0))
    for (cname, X, Y) in corners:
        ax.text(X, Y, cname, fontsize=13,
                ha='center', va='bottom',
                transform=tax.get_axes().transAxes)

    # Draw lines
    tax.horizontal_line(40, color='black')
    tax.horizontal_line(90, color='black')
    tax.left_parallel_line(90, color='black')
    tax.right_parallel_line(90, color='black')

    lines_ends = (((5,5,90), (5,90,5)),
                  ((5,90,5), (90,5,5)),
                  ((90,5,5), (5,5,90)),
                  ((50,0,50), (30,40,30)))
    for le in lines_ends:
        tax.line(le[0], le[1], color='black')

    # Plotting fields numbers
    symbols = (('01', (2.5,95,2.5)),   ('02', (2,65,33)),
               ('03', (17.5,65,17.5)), ('04', (33,65,2)),
               ('05', (2,22.5,75.5)),  ('06', (22.5,22.5,55)),
               ('07', (55,22.5,22.5)), ('08', (75.5,22.5,2)),
               ('09', (2.5,5,92.5)),   ('10', (28.5,2.5,69)),
               ('11', (69,2.5,28.5)),  ('12', (92.5,5,2.5)))

    fieldNames = ('dunite', 'px peridotite', 'px hbl peridotite',
                  'hbl peridotite', 'olivine pyroxenite',
                  'olivine hornblende\npyroxenite',
                  'olivine pyroxene\nhornblendite',
                  'olivine hornblendite', 'pyroxenite',
                  'hbl pyroxenite', 'px hornblendite',
                  'hornblendite')

    for (sym, pos), name in zip(symbols, fieldNames):
        tax.plot([pos], color='black', marker='${}$'.format(sym),
                     markersize=8, label=name, linestyle='None')

    # Show fields legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[:6], labels[:6], loc='upper left',                        # First column
              bbox_to_anchor=(0, 1.05), framealpha=0, fontsize=7)

    leg2 = Legend(ax, handles[6:], labels[6:], loc = 'upper right',             # Second column
                  bbox_to_anchor=(1, 1.05), framealpha=0, fontsize=7)
    ax.add_artist(leg2)

    return fig, tax


def CpxOlOpx_plot(ax, gridon, tickson):

    # Generate figure
    fig, tax = ternary.figure(ax=ax, scale=100)

    # Draw Boundary and Gridlines
    tax.boundary(linewidth=2.0)
    if gridon:
        tax.gridlines(color="black", multiple=5, linewidth=0.5)

    # Set ticks
    if tickson:
        tax.ticks(multiple=10, axis='lbr', linewidth=1, offset=0.015, fontsize=7)

    # Set corners labels
    corners = (('Ol', 0.5, 1.01), ('Opx', 0, 0), ('Cpx', 1, 0))
    for (cname, X, Y) in corners:
        ax.text(X, Y, cname, fontsize=13,
                ha='center', va='bottom',
                transform=tax.get_axes().transAxes)

    # Draw lines
    tax.horizontal_line(40, color='black')
    tax.horizontal_line(90, color='black')
    tax.left_parallel_line(90, color='black')
    tax.right_parallel_line(90, color='black')

    lines_ends = (((5,5,90), (5,90,5)),
                  ((5,90,5), (90,5,5)),
                  ((90,5,5), (5,5,90)))
    for le in lines_ends:
        tax.line(le[0], le[1], color='black')

    # Plotting fields numbers
    symbols = (('01', (2.5,95,2.5)),      ('02', (2,65,33)),
               ('03', (17.5,65,17.5)),    ('04', (33,65,2)),
               ('05', (2,22.5,75.5)),     ('06', (38.75,22.5,38.75)),
               ('07', (75.5,22.5,2)),     ('08', (2.5,5,92.5)),
               ('09', (48.75,2.5,48.75)), ('10', (92.5,5,2.5)))

    fieldNames = ('dunite', 'harzburgite', 'lherzolite', 'wehrlite',
                  'olivine orthopyroxenite', 'olivine websterite',
                  'olivine clinopyroxenite', 'orthopyroxenite', 'websterite',
                  'clinopyroxenite')

    for (sym, pos), name in zip(symbols, fieldNames):
        tax.plot([pos], color='black', marker='${}$'.format(sym),
                     markersize=8, label=name, linestyle='None')

    # Show fields legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[:5], labels[:5], loc='upper left',                        # First column
              bbox_to_anchor=(0, 1.05), framealpha=0, fontsize=7)

    leg2 = Legend(ax, handles[5:], labels[5:], loc = 'upper right',             # Second column
                  bbox_to_anchor=(1, 1.05), framealpha=0, fontsize=7)
    ax.add_artist(leg2)

    return fig, tax


def OlPlPx_plot(ax, gridon, tickson):

    # Generate figure
    fig, tax = ternary.figure(ax=ax, scale=100)

    # Draw Boundary and Gridlines
    tax.boundary(linewidth=2.0)
    if gridon:
        tax.gridlines(color="black", multiple=5, linewidth=0.5)

    # Set ticks
    if tickson:
        tax.ticks(multiple=10, axis='lbr', linewidth=1, offset=0.015, fontsize=7)

    # Set corners labels
    corners = (('Pl', 0.5, 1.01), ('Px', 0, 0), ('Ol', 1, 0))
    for (cname, X, Y) in corners:
        ax.text(X, Y, cname, fontsize=13,
                ha='center', va='bottom',
                transform=tax.get_axes().transAxes)

    # Draw lines
    tax.horizontal_line(10, color='black')
    tax.horizontal_line(90, color='black')
    tax.horizontal_line(35, color='black', linestyle='--', linewidth=0.5)
    tax.horizontal_line(65, color='black', linestyle='--', linewidth=0.5)
    tax.line((5,10,85), (5,90,5), color='black')
    tax.line((5,90,5), (85,10,5), color='black')

    # Plotting fields numbers
    symbols = (('01', (2.5,95,2.5)), ('02', (2.5,50,47.5)),
               ('03', (25,50,25)),   ('04', (47.5,50,2.5)),
               ('05', (47.5,5,47.5)))

    fieldNames = ('anorthosite', 'gabbro\ngabbronorite\nnorite',
                  'olivine gabbro\nolivine gabbronorite\nolivine norite',
                  'troctolite', 'plag-bearing\nultramafic rocks')

    for (sym, pos), name in zip(symbols, fieldNames):
        tax.plot([pos], color='black', marker='${}$'.format(sym),
                     markersize=8, label=name, linestyle='None')

    # Show fields legend
    ax.legend(loc='upper left', bbox_to_anchor=(0, 1.05),
              fontsize=7, framealpha=0)

    return fig, tax


def HblPlPx_plot(ax, gridon, tickson):

    # Generate figure
    fig, tax = ternary.figure(ax=ax, scale=100)

    # Draw Boundary and Gridlines
    tax.boundary(linewidth=2.0)
    if gridon:
        tax.gridlines(color="black", multiple=5, linewidth=0.5)

    # Set ticks
    if tickson:
        tax.ticks(multiple=10, axis='lbr', linewidth=1, offset=0.015, fontsize=7)

    # Set Axis labels
    corners = (('Pl', 0.5, 1.01), ('Px', 0, 0), ('Hbl', 1, 0))
    for (cname, X, Y) in corners:
        ax.text(X, Y, cname, fontsize=13,
                ha='center', va='bottom',
                transform=tax.get_axes().transAxes)

    # Draw lines
    tax.horizontal_line(10, color='black')
    tax.horizontal_line(35, color='black', linestyle='--', linewidth=0.5)
    tax.horizontal_line(65, color='black', linestyle='--', linewidth=0.5)
    tax.horizontal_line(90, color='black')
    tax.left_parallel_line(90, color='black')
    tax.right_parallel_line(90, color='black')

    lines_ends = (((5,10,85), (5,90,5)),
                  ((5,90,5), (85,10,5)),
                  ((50,0,50), (45,10,45)))
    for le in lines_ends:
        tax.line(le[0], le[1], color='black')

    # Plotting fields numbers
    symbols = (('01', (2.5,95,2.5)), ('02', (2.5,50,47.5)),
               ('03', (25,50,25)),   ('04', (47.5,50,2.5)),
               ('05', (2.5,5,92.5)), ('06', (26,5,69)),
               ('07', (69,5,26)),    ('08', (92.5,5,2.5)))

    fieldNames = ('anorthosite', 'gabbro\ngabbronorite\nnorite',
                  'px hbl gabbro\npx hbl gabbronorite\npx hbl norite',
                  'hbl gabbro', 'plagioclase-bearing\npyroxenite',
                  'plagioclase-bearing\nhbl pyroxenite',
                  'plagioclase-bearing\npx hornblendite',
                  'plagioclase-bearing\nhornblendite')

    for (sym, pos), name in zip(symbols, fieldNames):
        tax.plot([pos], color='black', marker='${}$'.format(sym),
                     markersize=8, label=name, linestyle='None')

    # Show fields legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[:4], labels[:4], loc='upper left',                        # First column
              bbox_to_anchor=(0, 1.05), framealpha=0, fontsize=7)

    leg2 = Legend(ax, handles[4:], labels[4:], loc = 'upper right',             # Second column
                  bbox_to_anchor=(1, 1.05), framealpha=0, fontsize=7)
    ax.add_artist(leg2)

    return fig, tax


def CpxPlOpx_plot(ax, gridon, tickson):

    # Generate figure
    fig, tax = ternary.figure(ax=ax, scale=100)

    # Draw Boundary and Gridlines
    tax.boundary(linewidth=2.0)
    if gridon:
        tax.gridlines(color="black", multiple=5, linewidth=0.5)

    # Set ticks
    if tickson:
        tax.ticks(multiple=10, axis='lbr', linewidth=1, offset=0.015, fontsize=7)

    # Set Axis labels
    corners = (('Pl', 0.5, 1.01), ('Opx', 0, 0), ('Cpx', 1, 0))
    for (cname, X, Y) in corners:
        ax.text(X, Y, cname, fontsize=13,
                ha='center', va='bottom',
                transform=tax.get_axes().transAxes)

    # Draw lines
    tax.horizontal_line(10, color='black')
    tax.horizontal_line(35, color='black', linestyle='--', linewidth=0.5)
    tax.horizontal_line(65, color='black', linestyle='--', linewidth=0.5)
    tax.horizontal_line(90, color='black')

    lines_ends = (((5,10,85), (5,90,5)),
                  ((5,90,5), (85,10,5)),
                  ((45,10,45), (5,90,5)))
    for le in lines_ends:
        tax.line(le[0], le[1], color='black')

    # Plotting fields numbers
    symbols = (('01', (2.5,95,2.5)),   ('02', (2.5,50,47.5)),
               ('03', (14.5,50,35.5)), ('04', (35.5,50,14.5)),
               ('05', (47.5,50,2.5)),  ('06', (47.5,5,47.5)))

    fieldNames = ('anorthosite', 'norite', 'cpx norite', 'opx gabbro', 'gabbro',
                  'plagioclase-bearing\npyroxenite')

    for (sym, pos), name in zip(symbols, fieldNames):
        tax.plot([pos], color='black', marker='${}$'.format(sym),
                     markersize=8, label=name, linestyle='None')

    # Show fields legend
    ax.legend(loc='upper left', bbox_to_anchor=(0, 1.05),
              framealpha=0, fontsize=7)

    return fig, tax


#WINDOW E WIDGET--------------------------------------------------------------------(PYQT4)----------------------------------------------------------------------------

class Window(QW.QMainWindow):

        def __init__(self):

            self.triangleChoice = "QAP"
            self.Image = True
            self.plotGrid = True
            self.plotTicks = True


            self.qtz = 0
            self.kfel = 0
            self.pl = 0
            self.foid = 0
            self.maf1 = 0
            self.maf2 = 0

            super(Window, self).__init__()
            self.setGeometry(30,75, 1300,600)
            self.showMaximized()
            self.setWindowTitle("Auto - QAPF Plutonic")
            self.setWindowIcon(QG.QIcon(str(ICONS_DIR / "QAPF.png")))
            self.statusBar()

            # Per aprire un file di testo (from ArcGIS MLC)
            openfileAction = QW.QAction("&Import from ArcGIS MLC table", self)
            openfileAction.setShortcut("Ctrl+I")
            openfileAction.setStatusTip("Import modal percentages in text format from ArcGIS Maximum Likelihood Classification attribute table.")
            openfileAction.triggered.connect(self.open_file)

            # Per cancellare la cronologia
            clearAction = QW.QAction("&Delete history", self)
            clearAction.setShortcut("Ctrl+D")
            clearAction.setStatusTip("Delete all previous classifications.")
            clearAction.triggered.connect(self.clear_history)

            # Per uscire dal programma
            extractAction = QW.QAction("&Exit", self)
            extractAction.setShortcut("Ctrl+Q")
            extractAction.setStatusTip("Close the program.")
            extractAction.triggered.connect(self.close_application)

            # Per modificare il colore dell'output
            change_colorAction = QW.QAction("&Change output colour", self)
            change_colorAction.setShortcut("Ctrl+Shift+C")
            change_colorAction.setStatusTip("Change the colour of the displayed rock name.")
            change_colorAction.triggered.connect(self.change_color)

            # Per modificare il font dell'output
            change_fontAction = QW.QAction("&Change output font", self)
            change_fontAction.setShortcut("Ctrl+Shift+F")
            change_fontAction.setStatusTip("Change the font of the displayed rock name.")
            change_fontAction.triggered.connect(self.change_font)

            # Per abilitare la griglia nei plots
            gridonAction = QW.QAction("&Show grid", self)
            gridonAction.setShortcut("Ctrl+Shift+G")
            gridonAction.setStatusTip("Enable/disable plots grid.")
            gridonAction.setCheckable(True)
            gridonAction.setChecked(True)
            gridonAction.triggered.connect(self.toggleGrid)

            # Per abilitare i ticks nei plots
            ticksonAction = QW.QAction("&Show ticks", self)
            ticksonAction.setShortcut("Ctrl+Shift+T")
            ticksonAction.setStatusTip("Enable/disable plots ticks.")
            ticksonAction.setCheckable(True)
            ticksonAction.setChecked(True)
            ticksonAction.triggered.connect(self.toggleTicks)

            # Per aprire la guida(EN)
            ENshow_guideAction = QW.QAction("&Show guide_EN", self)
            ENshow_guideAction.setShortcut("Alt+Shift+E")
            ENshow_guideAction.setStatusTip("Show a simple guide to the program (english version).")
            ENshow_guideAction.triggered.connect(self.show_guideEN)

            # Per aprire la guida(IT)
            ITshow_guideAction = QW.QAction("&Show guide_IT", self)
            ITshow_guideAction.setShortcut("Alt+Shift+I")
            ITshow_guideAction.setStatusTip("Show a simple guide to the program (italian version).")
            ITshow_guideAction.triggered.connect(self.show_guideIT)

            # Creazione del menu
            # File = (apri file + cancella cronologia + esci dal programma),
            # Edit = (cambia colore + cambia font + Plots submenu = (griglia grafico, ticks grafico)),
            # Help = (apri guida_EN + (apri guida_IT)
            if mainMenu := self.menuBar():
                if fileMenu := mainMenu.addMenu('&File'):
                    fileMenu.addAction(openfileAction)
                    fileMenu.addAction(clearAction)
                    fileMenu.addAction(extractAction)
                if editMenu := mainMenu.addMenu('&Edit'):
                    editMenu.addAction(change_colorAction)
                    editMenu.addAction(change_fontAction)
                    if plot_subMenu := editMenu.addMenu('&Plots'):
                        plot_subMenu.addAction(gridonAction)
                        plot_subMenu.addAction(ticksonAction)
                if helpMenu := mainMenu.addMenu('&Help'):
                    helpMenu.addAction(ENshow_guideAction)
                    helpMenu.addAction(ITshow_guideAction)

            cWidget = QW.QWidget(self)

            # 1.1 QAP/APF
            QorF = QW.QComboBox(self)
            QorF.addItem("Q-A-P")
            QorF.addItem("A-P-F")
            QorF.setStatusTip("Switch from Upper Triangle (Q-A-P) to Lower Triangle (A-P-F).")
            QorF.activated[str].connect(self.triangle_choice)
            # 1.2 Immagine YES/NO
            checkBoxImage = QW.QCheckBox("Display Diagram")
            checkBoxImage.setStatusTip("Display the QAPF diagram at the end of the classification.")
            checkBoxImage.toggle()
            checkBoxImage.stateChanged.connect(self.active_images)
            # 1.3 Clear buttons
            clear_Btn = QW.QPushButton("Clear values", cWidget)
            clear_Btn.setStatusTip("Clear all the indices.")
            clear_Btn.clicked.connect(self.clear_values)

            # 1 Prima box verticale (QAP/APF + Immagine YES/NO + clear button)
            vBox1 = QW.QVBoxLayout()
            vBox1.setSpacing(2)
            vBox1.addWidget(QorF)
            vBox1.addWidget(checkBoxImage)
            vBox1.addWidget(clear_Btn)


            # 2.1.1 Plot1 Box (Primi Toolbar Matplotlib e Canvas)
            self.figurePlot1 = Figure()
            self.ax1 = self.figurePlot1.add_subplot(111)
            self.ax1.axis('off')
            self.canvas1 = FigureCanvas(self.figurePlot1)
            self.mplToolbar1 = NavTbar(self.canvas1, self)
            customizeBtn = self.mplToolbar1.findChildren(QW.QAction)[8]
            self.mplToolbar1.removeAction(customizeBtn)
            plot1box = QW.QVBoxLayout()
            plot1box.addWidget(self.canvas1)
            plot1box.addWidget(self.mplToolbar1)
            # 2.1.2 Plot2 Box (Secondi Toolbar Matplotlib e Canvas)
            self.figurePlot2 = Figure()
            self.ax2 = self.figurePlot2.add_subplot(111)
            self.ax2.axis('off')
            self.canvas2 = FigureCanvas(self.figurePlot2)
            self.mplToolbar2 = NavTbar(self.canvas2, self)
            customizeBtn = self.mplToolbar2.findChildren(QW.QAction)[8]
            self.mplToolbar2.removeAction(customizeBtn)
            plot2box = QW.QVBoxLayout()
            plot2box.addWidget(self.canvas2)
            plot2box.addWidget(self.mplToolbar2)
            # 2.1 Box orizzontale dei plot (Plot1 Box + Plot2 Box)
            plotsBox = QW.QHBoxLayout()
            plotsBox.addLayout(plot1box)
            plotsBox.addLayout(plot2box)

            # 2.2 Finestra di output del risultato
            self.resultShow = QW.QTextEdit(cWidget)
            self.resultShow.setReadOnly(True)
            self.resultShow.setStyleSheet('color: blue')
            font = QG.QFont()
            font.setPointSize(9)
            self.resultShow.setFont(font)

            # 2 Seconda box verticale (PlotsBox + finestra output)
            vBox2 = QW.QVBoxLayout()
            vBox2.setSpacing(2)
            vBox2.addLayout(plotsBox)
            vBox2.addWidget(self.resultShow)


            # 3.1.1 Q_Btn
            Q_Btn = QW.QPushButton("Q", cWidget)
            Q_Btn.setStatusTip("Quartz.")
            Q_Btn.clicked.connect(self.Q_insertValue)
            # 3.1.2 Q_Label
            self.Q_Label = QW.QLabel("0.0%", cWidget)
            # 3.1 Q_Box (Q_Btn + Q_Label)
            Q_Box = QW.QHBoxLayout()
            Q_Box.setSpacing(4)
            Q_Box.addWidget(Q_Btn)
            Q_Box.addWidget(self.Q_Label)

            # 3.2.1 A_Btn
            A_Btn = QW.QPushButton("A", cWidget)
            A_Btn.setStatusTip("Alkali-feldspar (+ albite).")
            A_Btn.clicked.connect(self.A_insertValue)
            # 3.2.2 A_Label
            self.A_Label = QW.QLabel("0.0%", cWidget)
            # 3.2 A_Box (A_Btn + A_Label)
            A_Box = QW.QHBoxLayout()
            A_Box.setSpacing(4)
            A_Box.addWidget(A_Btn)
            A_Box.addWidget(self.A_Label)

            # 3.3.1 P_Btn
            P_Btn = QW.QPushButton("P", cWidget)
            P_Btn.setStatusTip("Plagioclase (- albite).")
            P_Btn.clicked.connect(self.P_insertValue)
            # 3.3.2 P_Label
            self.P_Label = QW.QLabel("0.0%", cWidget)
            # 3.3 P_Box (P_Btn + P_Label)
            P_Box = QW.QHBoxLayout()
            P_Box.setSpacing(4)
            P_Box.addWidget(P_Btn)
            P_Box.addWidget(self.P_Label)

            # 3.4.1 F_Btn
            F_Btn = QW.QPushButton("F", cWidget)
            F_Btn.setStatusTip("Feldspathoid.")
            F_Btn.clicked.connect(self.F_insertValue)
            # 3.4.2 F_Label
            self.F_Label = QW.QLabel("0.0%", cWidget)
            # 3.4 F_Box (F_Btn + F_Label)
            F_Box = QW.QHBoxLayout()
            F_Box.setSpacing(4)
            F_Box.addWidget(F_Btn)
            F_Box.addWidget(self.F_Label)

            # 3.5.1 M1_Btn
            M1_Btn = QW.QPushButton("M'", cWidget)
            M1_Btn.setStatusTip("Coloured mafic and related minerals (colour index modifiers).")
            M1_Btn.clicked.connect(self.M1_insertValue)
            # 3.5.2 M1_Label
            self.M1_Label = QW.QLabel("0.0%", cWidget)
            # 3.5 M1_Box (M1_Btn + M1_Label)
            M1_Box = QW.QHBoxLayout()
            M1_Box.setSpacing(4)
            M1_Box.addWidget(M1_Btn)
            M1_Box.addWidget(self.M1_Label)

            # 3.6.1 M2_Btn
            M2_Btn = QW.QPushButton("M''", cWidget)
            M2_Btn.setStatusTip("Colourless mafic and related minerals.")
            M2_Btn.clicked.connect(self.M2_insertValue)
            # 3.6.2 M2_Label
            self.M2_Label = QW.QLabel("0.0%", cWidget)
            # 3.6 M2_Box (M2_Btn + M2_Label)
            M2_Box = QW.QHBoxLayout()
            M2_Box.setSpacing(4)
            M2_Box.addWidget(M2_Btn)
            M2_Box.addWidget(self.M2_Label)

            # 3.7 tot_Label
            self.tot_Label = QW.QLabel("Total: 0% / 100.0%", cWidget)
            self.tot_Label.setStyleSheet('color: red')

            # 3.8 START
            start_Btn = QW.QPushButton("START", cWidget)
            font.setPointSize(13)
            start_Btn.setFont(font)
            start_Btn.setStatusTip("Start classification.")
            start_Btn.clicked.connect(self.start_classification)

            # 3 Terza box verticale (Q_Box + A_Box + P_Box + F_Box + M1_Box + M2_Box + tot_Label + start button)
            vBox3 = QW.QVBoxLayout()
            vBox3.setSpacing(2)
            vBox3.addLayout(Q_Box)
            vBox3.addLayout(A_Box)
            vBox3.addLayout(P_Box)
            vBox3.addLayout(F_Box)
            vBox3.addLayout(M1_Box)
            vBox3.addLayout(M2_Box)
            vBox3.addWidget(self.tot_Label)
            vBox3.addWidget(start_Btn)

            # Layout principale (prima box verticale + finestra di output del risultato + seconda box verticale)
            hBox = QW.QHBoxLayout()
            hBox.setSpacing(5)
            hBox.addLayout(vBox1)
            hBox.addLayout(vBox2)
            hBox.addLayout(vBox3)

            cWidget.setLayout(hBox)
            self.setCentralWidget(cWidget)

#---------------------------------------------------------------------------CAMPO DEGLI ADD-ON-------------------------------------------------------------------------

#Lista dei feldspatoidi------------------------------------------------------------------------------------------------------------------------------------------------
        def foid_type(self):

            txt = "Please select the predominant foid in your sample"
            self.DialogWindow('INFO', "Choose the foid", txt)

            while True:
                foid_name, ok = QW.QInputDialog.getItem(
                    self, "Predominant foid", "Foids list:", FOIDS, 0, False)

                if ok and foid_name:
                    return foid_name


#Richiesta della quantita' di Anortite nei plagioclasi------------------------------------------------------------------------------------------------------------------
        def An_value(self):

            choice = QW.QMessageBox.question(
                self, "Anorthite percentage",
                "Do you know the average content of anorthite in plagioclase?",
                QW.QMessageBox.Yes | QW.QMessageBox.No, QW.QMessageBox.No
            )
            if choice == QW.QMessageBox.Yes:
                an, ok = QW.QInputDialog.getDouble(
                    self, "Anorthite percentage", self.tr("Insert an%:"), 0, 0, 100, 1)
                if ok:
                    return an
            return None


#DIAGRAMMI ROCCE ULTRAMAFICHE------------------------------------------------------------------------------------------------------------------------------------------
        def ultramafic_rock(self):

            self.DialogWindow(
                'INFO',
                "Ultramafic rocks diagrams",
                "Insert the modal percentages (NOT recalculated) of the following minerals."
            )
            amounts = dict().fromkeys(ULTRAMAFIC_MINERALS, 0.0)
            tot = self.maf1
            while tot == self.maf1:
                for m in amounts.keys():
                    while True:
                        perc, ok = QW.QInputDialog.getDouble(
                            self, MINERAL_ABBREVIATIONS.get(m),
                            self.tr(f"{m} %:\t\t(M' remaining = {round(tot, 1)}% / {self.maf1}%)"),
                            0, 0, tot, 1
                        )
                        if ok:
                            amounts[m] = perc
                            tot -= perc
                            break

                if tot == self.maf1:
                    self.DialogWindow(
                        'CRIT', "Index Error", "Insert at least one value!")

            ol, opx, cpx, hbl, sp, grt = amounts.values()
            px = cpx + opx

            ol_ric = (ol * 100.0) / (ol + px + hbl)
            cpx_ric = (cpx * 100.0) / (ol + px + hbl)
            opx_ric = (opx * 100.0) / (ol + px + hbl)
            px_ric = cpx_ric + opx_ric
            hbl_ric = (hbl * 100.0) / (ol + px + hbl)

            #per classificazione extra di PERIDOTITI!
            add = ""
            if self.pl == 0.0 and sp == 0.0 and grt == 0.0:
                add = ""
            elif self.pl > sp and self.pl > grt:
                if self.pl <= 5.0:
                    add = "[Plagioclase-bearing] "
                else:
                    add = "[Plagioclase] "
            elif sp >= self.pl and sp > grt:
                if sp <= 5.0:
                    add = "[Spinel-bearing] "
                else:
                    add = "[Spinel] "
            elif grt >= self.pl and grt >= sp:
                if grt <= 5.0:
                    add = "[Garnet-bearing] "
                else:
                    add = "[Garnet] "


            #diagramma OL-CPX-OPX
            if hbl == 0.0:
                self.drawPlot(CpxOlOpx_plot, [(cpx_ric, ol_ric, opx_ric)])

                if cpx_ric >= 90.0:
                    name = "Clinopyroxenite"
                elif opx_ric >= 90.0:
                    name = "Orthopyroxenite"
                elif ol_ric < 5.0 and opx_ric < 90.0 and cpx_ric < 90.0:
                    name = "Websterite"
                elif 5.0 <= ol_ric < 40.0:
                    if cpx_ric < 5.0:
                        name = "Olivine orthopyroxenite"
                    elif opx_ric < 5.0:
                        name = "Olivine clinopyroxenite"
                    else:
                        name = "Olivine websterite"
                else:
                    if ol_ric >= 90.0:
                        name = add + "Dunite"
                    elif cpx_ric < 5.0:
                        name = add + "Harzburgite"
                    elif opx_ric < 5.0:
                        name = add + "Wehrlite"
                    else:
                        name = add + "Lherzolite"


            #diagramma OL-PX-HBL
            else:
                self.drawPlot(HblOlPx_plot, [(hbl_ric, ol_ric, px_ric)])

                if hbl_ric >= 90.0:
                    name = "Hornblendite"
                elif px_ric >= 90.0:
                    name = "Pyroxenite"
                elif ol_ric < 5.0 and px_ric < 90.0 and hbl_ric < 90.0:
                    if px_ric > hbl_ric:
                        name = "Hornblende pyroxenite"
                    elif px_ric < hbl_ric:
                        name = "Pyroxene hornblendite"
                    else:
                        name = "Pyroxene hornblendite//hornblende pyroxenite"
                elif 5.0 <= ol_ric < 40.0:
                    if hbl_ric < 5.0:
                        name = "Olivine pyroxenite"
                    elif px_ric < 5.0:
                        name = "Olivine hornblendite"
                    else:
                        if px_ric > hbl_ric:
                            name = "Olivine hornblende pyroxenite"
                        elif px_ric < hbl_ric:
                            name = "Olivine pyroxene hornblendite"
                        else:
                            name = "Olivine hornblende pyroxenite//olivine pyroxene hornblendite"
                else:
                    if ol_ric >= 90.0:
                        name = add + "Dunite"
                    elif hbl_ric < 5.0:
                        name = add + "Pyroxene peridotite"
                    elif px_ric < 5.0:
                        name = add + "Hornblende peridotite"
                    else:
                        name = add + "Pyroxene hornblende peridotite"


            return name

#DIAGRAMMI DEI GABBRI--------------------------------------------------------------------------------------------------------------------------------------------------
        def Gabbro_diagrams(self):
            use_gabbroic_diagrams = QW.QMessageBox.question(self,
                                                               "Gabbroic rock",
                                                               "This is a gabbroic rock. Do you want to use the gabbroic rocks diagrams for a better classification?",
                                                               QW.QMessageBox.Yes | QW.QMessageBox.No,QW.QMessageBox.No)
            if use_gabbroic_diagrams == QW.QMessageBox.No:
                return "Gabbroid"
            else:
                self.DialogWindow(
                    'INFO', "Gabbroic rocks diagrams",
                    "Insert the modal percentages (NOT recalculated) of the following minerals."
                )
                amounts = dict().fromkeys(GABBRO_MINERALS, 0.0)
                tot = self.maf1
                for m in amounts.keys():
                    while True:
                        perc, ok = QW.QInputDialog.getDouble(
                            self, MINERAL_ABBREVIATIONS.get(m),
                            self.tr(f"{m} %:\t\t(M' remaining = {round(tot, 1)}% / {self.maf1}%)"),
                            0, 0, tot, 1
                        )
                        if ok:
                            amounts[m] = perc
                            tot -= perc
                            break
                if tot == self.maf1:
                    self.DialogWindow(
                        'WARN',
                        "Classification with lack of accuracy",
                        "You didn't insert any value: the classification may be wrong or not really accurate."
                    )

                ol, opx, cpx, hbl = amounts.values()
                px = opx + cpx

                #il root e' un valore da aggiungere in alcuni nomi successivi
                if opx < cpx:
                    root = "Gabbro"
                elif opx == cpx:
                    root = "Gabbronorite"
                else:
                    root = "Norite"

                #diagramma PL-CPX-OPX
                if ol == 0.0 and hbl == 0.0:
                    cpx_ric = (cpx*100.0)/(px + self.pl)
                    opx_ric = (opx*100.0)/(px + self.pl)
                    px_ric = cpx_ric + opx_ric
                    pl_ric = (self.pl*100.0)/(px + self.pl)

                    self.drawPlot(CpxPlOpx_plot, [(cpx_ric, pl_ric, opx_ric)], mainPlot=False)

                    if px_ric > 90.0:                                           # this rock will not appear in the classification, because treated as ultramafic
                        gabbro_type = "Plagioclase-bearing pyroxenite"

                    elif px_ric <= 10.0:
                        gabbro_type = "Anorthosite"

                    else:
                        if cpx_ric <= 5.0:
                            gabbro_type = "Norite"
                        elif opx_ric <= 5.0:
                            gabbro_type = "Gabbro"
                        else:
                            if opx_ric > cpx_ric:
                                gabbro_type = "Clinopyroxene norite"
                            elif opx_ric < cpx_ric:
                                gabbro_type = "Orthopyroxene gabbro"
                            else:
                                gabbro_type = "Gabbronorite"


                #diagramma PL-PX-OL
                elif ol > hbl:
                    cpx_ric = (cpx*100.0)/(px + ol + self.pl)
                    opx_ric = (opx*100.0)/(px + ol + self.pl)
                    px_ric = cpx_ric + opx_ric
                    ol_ric = (ol*100.0)/(px + ol + self.pl)
                    pl_ric = (self.pl*100.0)/(px + ol + self.pl)

                    self.drawPlot(OlPlPx_plot,
                                  [(ol_ric, pl_ric, px_ric)],
                                  mainPlot=False)

                    if px_ric + ol_ric > 90.0:                                  # this rock will not appear in the classification, because treated as ultramafic
                        gabbro_type = "Plagioclase-bearing ultramafic rock"

                    elif px_ric + ol_ric <= 10.0:
                        gabbro_type = "Anorthosite"

                    else:
                        if ol_ric <= 5.0:
                            gabbro_type = root
                        elif px_ric <= 5.0:
                            gabbro_type = "Troctolite"
                        else:
                            gabbro_type = "Olivine " + root.lower()

                #diagramma PL-PX-HBL
                else:
                    cpx_ric = (cpx*100.0)/(px + hbl + self.pl)
                    opx_ric = (opx*100.0)/(px + hbl + self.pl)
                    px_ric = cpx_ric + opx_ric
                    hbl_ric = (hbl*100.0)/(px + hbl + self.pl)
                    pl_ric = (self.pl*100.0)/(px + hbl + self.pl)

                    self.drawPlot(HblPlPx_plot,
                                  [(hbl_ric, pl_ric, px_ric)],
                                  mainPlot=False)

                    if px_ric + hbl_ric > 90.0:                                 # all of these rocks names will not appear in the classification, because treated as ultramafic
                        if px_ric >= 90.0:
                            gabbro_type = "Plagioclase-bearing pyroxenite"
                        elif hbl_ric >= 90.0:
                            gabbro_type = "Plagioclase-bearing hornblendite"
                        else:
                            if px_ric > hbl_ric:
                                gabbro_type = "Plagioclase-bearing hornblende pyroxenite"
                            elif px_ric < hbl_ric:
                                gabbro_type = "Plagioclase-bearing pyroxene hornblendite"
                            else:
                                gabbro_type = "Plag.-bearing hornblende pyroxenite//plag.-bearing pyroxene hornblendite"

                    elif px_ric + hbl_ric <= 10.0:
                        gabbro_type = "Anorthosite"

                    else:
                        if px_ric <= 5.0:
                            gabbro_type = "Hornblende gabbro"
                        elif hbl_ric <= 5.0:
                            gabbro_type = root
                        else:
                            if px_ric > hbl_ric:
                                gabbro_type = "Pyroxene hornblende " + root.lower()
                            else:
                                gabbro_type = "Hornblende pyroxene " + root.lower()


                return str(gabbro_type)

##TRIANGOLO SUPERIORE----------------------------------------------------------------(QAP)-----------------------------------------------------------------------------

        #Quartzolite
        def Field_1a(self):
            name = "Quartzolite"
            return name

        #Quartz-rich Granitoid
        def Field_1b(self):
            name = "Quartz-rich granitoid"
            return name

        #Alkali feldspar granite
        def Field_2(self):
            sodic_terms = QW.QMessageBox.question(self,"Sodic terms",
                                                     "Does your sample contain sodic amphibols and/or sodic pyroxenes?",
                                                     QW.QMessageBox.Yes | QW.QMessageBox.No,QW.QMessageBox.No)
            if sodic_terms == QW.QMessageBox.Yes:
                name = "Peralkaline granite"
            else:
                if self.maf1 < 10.0:
                    name = "(Leuco-) alkali-feldspar granite\t{special term = alaskite}"
                elif 10.0 <= self.maf1 < 20.0:
                    name = "Alkali-feldspar granite"
                else:
                    name = "(Mela-) alkali-feldspar granite"

            return name

        #Syeno-granite
        def Field_3a(self):
            if self.maf1 < 5.0:
                name = "(Leuco-) syeno-granite"
            elif 5.0 <= self.maf1 < 20.0:
                name = "Syeno-granite"
            else:
                name = "(Mela-) syeno-granite"

            return name

        #Monzo-granite
        def Field_3b(self):
            if self.maf1 < 5.0:
                name = "(Leuco-) monzo-granite"
            elif 5.0 <= self.maf1 < 20.0:
                name = "Monzo-granite"
            else:
                name = "(Mela-) monzo-granite"

            return name

        #Granodiorite
        def Field_4(self):
            note = "Note that if the average composition of plagioclase is\
 an% = 50 - 100, this rock should be named 'granogabbro'"

            if self.maf1 < 5.0:
                name = "(Leuco-) granodiorite"
            elif 5.0 <= self.maf1 < 25.0:
                name = "Granodiorite"
            else:
                name = "(Mela-) granodiorite"

            return name, note

        #Tonalite
        def Field_5(self):
            if self.maf1 < 10.0:
                name = "(Leuco-) tonalite\t{special terms = trondhjemite or plagiogranite}"
            elif 10.0 <= self.maf1 < 40.0:
                name = "Tonalite"
            else:
                name = "(Mela-) tonalite"

            return name

        #Alkali feldspar syenite (+QTZ)
        def Field_6Q(self):
            if self.maf1 < 25.0:
                name = "Alkali-feldspar quartz syenite"
            else:
                name = "(Mela-) alkali-feldspar quartz syenite"

            return name

        #Syenite (+QTZ)
        def Field_7Q(self):
            if self.maf1 < 5.0:
                name = "(Leuco-) quartz syenite"
            elif 5.0 <= self.maf1 < 30.0:
                name = "Quartz syenite"
            else:
                name = "(Mela-) quartz syenite"

            return name

        #Monzonite (+qtz)
        def Field_8Q(self):
            if self.maf1 < 10.0:
                name = "(Leuco-) quartz monzonite"
            elif 10.0 <= self.maf1 < 35.0:
                name = "Quartz monzonite"
            else:
                name = "(Mela-) quartz monzonite"

            return name

        #Monzodiorite-monzogabbro (+QTZ)
        def Field_9Q(self):
            an = self.An_value()
            if an is not None:
                if an <= 50.0:
                    if self.maf1 < 15.0:
                        name = "(Leuco-) quartz monzodiorite"
                    elif 15.0 <= self.maf1 < 40.0:
                        name = "Quartz monzodiorite"
                    else:
                        name = "(Mela-) quartz monzodiorite"
                else:
                    if self.maf1 < 20.0:
                        name = "(Leuco-) quartz monzogabbro"
                    elif 20.0 <= self.maf1 < 50.0:
                        name = "Quartz monzogabbro"
                    else:
                        name = "(Mela-) quartz monzogabbro"
            else:
                if self.maf1 < 15.0:
                    name = "(Leuco-) quartz monzodiorite"
                elif 15.0 <= self.maf1 <= 20.0:
                    name = "Quartz monzodiorite"
                elif 20.0 < self.maf1 < 50.0:
                    name = "Quartz monzogabbro"
                else:
                    name = "(Mela-) quartz monzogabbro"

            return name

        #Anorthosite-diorite-gabbro (+QTZ)
        def Field_10Q(self):
            if self.pl >= 90.0:
                name = "Quartz anorthosite"

            else:
                an = self.An_value()
                if an is not None:
                    if an <= 50.0:
                        if self.maf1 < 20.0:
                            name = "(Leuco-) quartz diorite"
                        elif 20.0 <= self.maf1 < 45.0:
                            name = "Quartz diorite"
                        else:
                            name = "(Mela-) quartz diorite"
                    else:
                        if self.maf1 < 25.0:
                            name = "(Leuco-) quartz " + self.Gabbro_diagrams().lower()
                        elif 25.0 <= self.maf1 < 55.0:
                            name = "Quartz " + self.Gabbro_diagrams().lower()
                        else:
                            name = "(Mela-) quartz " + self.Gabbro_diagrams().lower()
                else:
                    if self.maf1 < 20.0:
                            name = "(Leuco-) quartz diorite"
                    elif 20.0 <= self.maf1 <= 25.0:
                        name = "Quartz diorite"
                    elif 25.0 < self.maf1 < 55.0:
                        name = "Quartz " + self.Gabbro_diagrams().lower()
                    else:
                        name = "(Mela-) quartz " + self.Gabbro_diagrams().lower()

            #costrutto per evitare la comparsa del termine (Leuco-) Anorthosite che perde di significato
            if '(Leuco-)' and 'anorthosite' in name:
                name = name.replace('(Leuco-) ', '')

            return name

        #Alkali feldspar syenite
        def Field_6(self):
            if self.maf1 < 25.0:
                name = "Alkali-feldspar syenite"
            else:
                name = "(Mela-) alkali-feldspar syenite"

            return name

        #Syenite
        def Field_7(self):
            if self.maf1 < 10.0:
                name = "(Leuco-) syenite"
            elif 10.0 <= self.maf1 < 35.0:
                name = "Syenite"
            else:
                name = "(Mela-) syenite"

            return name

        #Monzonite
        def Field_8(self):
            if self.maf1 < 15.0:
                name = "(Leuco-) monzonite"
            elif 15.0 <= self.maf1 < 45.0:
                name = "Monzonite"
            else:
                name = "(Mela-) monzonite"

            return name

        #Monzodiorite-monzogabbro
        def Field_9(self):
            an = self.An_value()
            if an is not None:
                if an <= 50.0:
                    if self.maf1 < 20.0:
                        name = "(Leuco-) monzodiorite"
                    elif 20.0 <= self.maf1 < 50.0:
                        name = "Monzodiorite"
                    else:
                        name = "(Mela-) monzodiorite"
                else:
                    if self.maf1 < 25.0:
                        name = "(Leuco-) monzogabbro"
                    elif 25.0 <= self.maf1 < 60.0:
                        name = "Monzogabbro"
                    else:
                        name = "(Mela-) monzogabbro"
            else:
                if self.maf1 < 20.0:
                    name = "(Leuco-) monzodiorite"
                elif 20.0 <= self.maf1 <= 25.0:
                    name = "Monzodiorite"
                elif 25.0 < self.maf1 < 60.0:
                    name = "Monzogabbro"
                else:
                    name = "(Mela-) monzogabbro"

            return name

        #Anorthosite-diorite-gabbro
        def Field_10(self):
            if self.pl >= 90.0:
                name = "Anorthosite"

            else:
                an = self.An_value()
                if an is not None:
                    if an <= 50.0:
                        if self.maf1 < 25.0:
                            name = "(Leuco-) diorite"
                        elif 25.0 <= self.maf1 < 50.0:
                            name = "Diorite"
                        else:
                            name = "(Mela-) diorite"
                    else:
                        if self.maf1 < 35.0:
                            name = "(Leuco-) " + self.Gabbro_diagrams().lower()
                        elif 35.0 <= self.maf1 < 65.0:
                            name = "" + self.Gabbro_diagrams()
                        else:
                            name = "(Mela-) " + self.Gabbro_diagrams().lower()

                else:
                    if self.maf1 < 25.0:
                        name = "(Leuco-) diorite"
                    elif 25.0 <= self.maf1 <= 35.0:
                        name = "Diorite"
                    elif 35.0 < self.maf1 < 65.0:
                        name = "" + self.Gabbro_diagrams()
                    else:
                        name = "(Mela-) " + self.Gabbro_diagrams().lower()

            #costrutto per evitare la comparsa del termine (Leuco-) Anorthosite che perde di significato
            if '(Leuco-)' and 'anorthosite' in name:
                name = name.replace('(Leuco-) ', '')

            return name

##TRIANGOLO INFERIORE----------------------------------------------------------------(APF)-----------------------------------------------------------------------------

        #Alkali feldspar syenite (+FOID)
        def Field_6F(self):
            note = "Please note that the general term 'agpaite' may be used for peralkaline\
 varieties of this rock, characterized by complex Zr and Ti minerals such as eudialyte, rather\
 than simple minerals such as zircon and ilmenite."

            if self.maf1 < 25.0:
                name = self.foid_type() + "-bearing alkali-feldspar syenite"
            else:
                name = "(Mela-) " + self.foid_type().lower() + "-bearing alkali-feldspar syenite"

            return name, note

        #Syenite (+FOID)
        def Field_7F(self):
            if self.maf1 < 10.0:
                name = "(Leuco-) " + self.foid_type().lower() + "-bearing syenite"
            elif 10.0 <= self.maf1 < 35.0:
                name = self.foid_type() + "-bearing syenite"
            else:
                name = "(Mela-) " + self.foid_type().lower() + "-bearing syenite"

            return name

        #Monzonite (+FOID)
        def Field_8F(self):
            if self.maf1 < 15.0:
                name = "(Leuco-) " + self.foid_type().lower() + "-bearing monzonite"
            elif 15.0 <= self.maf1 < 45.0:
                name = self.foid_type() + "-bearing monzonite"
            else:
                name = "(Mela-) " + self.foid_type().lower() + "-bearing monzonite"

            return name

        #Monzodiorite-monzogabbro (+FOID)
        def Field_9F(self):
            an = self.An_value()
            if an is not None:
                if an <= 50.0:
                    if self.maf1 < 20.0:
                        name = "(Leuco-) " + self.foid_type().lower() + "-bearing monzodiorite"
                    elif 20.0 <= self.maf1 < 50.0:
                        name = self.foid_type() + "-bearing monzodiorite"
                    else:
                        name = "(Mela-) " + self.foid_type().lower() + "-bearing monzodiorite"
                else:
                    if self.maf1 < 25.0:
                        name = "(Leuco-) " + self.foid_type().lower() + "-bearing monzogabbro"
                    elif 25.0 <= self.maf1 < 60.0:
                        name = self.foid_type() + "-bearing monzogabbro"
                    else:
                        name = "(Mela-) " + self.foid_type().lower() + "-bearing monzogabbro"
            else:
                if self.maf1 < 20.0:
                    name = "(Leuco-) " + self.foid_type().lower() + "-bearing monzodiorite"
                elif 20.0 <= self.maf1 <= 25.0:
                    name = self.foid_type() + "-bearing monzodiorite"
                elif 25.0 < self.maf1 < 60.0:
                    name = self.foid_type() + "-bearing monzogabbro"
                else:
                    name = "(Mela-) " + self.foid_type().lower() + "-bearing monzogabbro"

            return name

        #Anorthosite-diorite-gabbro (+FOID)
        def Field_10F(self):
            if self.pl >= 90.0:
                name = self.foid_type() + "-bearing anorthosite"

            else:
                an = self.An_value()
                if an is not None:
                    if an <= 50.0:
                        if self.maf1 < 25.0:
                                name = "(Leuco-) " + self.foid_type().lower() + "-bearing diorite"
                        elif 25.0 <= self.maf1 < 50.0:
                            name = self.foid_type() + "-bearing diorite"
                        else:
                            name = "(Mela-) " + self.foid_type().lower() + "-bearing diorite"
                    else:
                        if self.maf1 < 35.0:
                            name = "(Leuco-) " + self.foid_type().lower() + "-bearing " + self.Gabbro_diagrams().lower()
                        elif 35.0 <= self.maf1 < 65.0:
                            name = self.foid_type() + "-bearing " + self.Gabbro_diagrams().lower()
                        else:
                            name = "(Mela-) " + self.foid_type().lower() + "-bearing " + self.Gabbro_diagrams().lower()
                else:
                    if self.maf1 < 25.0:
                            name = "(Leuco-) " + self.foid_type().lower() + "-bearing diorite"
                    elif 25.0 <= self.maf1 <= 35.0:
                        name = self.foid_type() + "-bearing diorite"
                    elif 35.0 < self.maf1 < 65.0:
                        name = self.foid_type() + "-bearing " + self.Gabbro_diagrams().lower()
                    else:
                        name = "(Mela-) " + self.foid_type().lower() + "-bearing " + self.Gabbro_diagrams().lower()

            #costrutto per evitare la comparsa del termine (Leuco-) Anorthosite che perde di significato
            if '(Leuco-)' and 'anorthosite' in name:
                name = name.replace('(Leuco-) ', '')

            return name

        #Foid syenite
        def Field_11(self):
            if self.maf1 < 30.0:
                name = self.foid_type() + " syenite"
            elif 30.0 <= self.maf1 < 60.0:
                name = "(Mela-) " + self.foid_type().lower() + " syenite\t{special term = malignite}"
            else:
                name = "(Mela-) " + self.foid_type().lower() + " syenite\t{special term = shonkinite}"

            return name

        #Foid monzosyenite
        def Field_12(self):
            note = "Please note that the term 'monzosyenite' can be replaced with 'plagisyenite'.\n\
Moreover note that if the average composition of plagioclase is an% = 10 - 30 (oligoclase), this rock can also be named 'miaskite'."

            if self.maf1 < 15.0:
                name = "(Leuco-) " + self.foid_type().lower() + " monzosyenite"
            elif 15.0 <= self.maf1 < 45.0:
                name = self.foid_type() + " monzosyenite"
            else:
                name = "(Mela-) " + self.foid_type().lower() + " monzosyenite"

            return name, note

        #Foid monzodiorite-monzogabbro
        def Field_13(self):
            note = "\t{special term = essexite}"

            an = self.An_value()
            if an is not None:
                if an <= 50.0:
                    if self.maf1 < 20.0:
                        name = "(Leuco-) " + self.foid_type().lower() + " monzodiorite"
                    elif 20.0 <= self.maf1 < 60.0:
                        name = self.foid_type() + " monzodiorite"
                    else:
                        name = "(Mela-) " + self.foid_type().lower() + " monzodiorite"
                else:
                    if self.maf1 < 20.0:
                        name = "(Leuco-) " + self.foid_type().lower() + " monzogabbro"
                    elif 20.0 <= self.maf1 < 60.0:
                        name = self.foid_type() + " monzogabbro"
                    else:
                        name = "(Mela-) " + self.foid_type().lower() + " monzogabbro"
            else:
                self.DialogWindow('WARN',
                                  "Classification with lack of accuracy",
                                  "It's not possible to accurately classificate this rock if the average content of anorthite is not provided.")
                if self.maf1 < 20.0:
                    name = r"(Leuco-) foid monzodiorite\monzogabbro"
                elif 20.0 <= self.maf1 < 60.0:
                    name = r"Foid monzodiorite\monzogabbro"
                else:
                    name = r"(Mela-) foid monzodiorite\monzogabbro"

            if "Nepheline" in name: #serve ad aggiungere la nota sull'Essexite che c'e' solo quando il nome e' "Nepheline..ecc.." (escludo i termini leuco e mela)
                name = name + note

            return name

        #Foid diorite-gabbro
        def Field_14(self):
            note1 = "\t{special term = theralite}"
            note2 = "\t{special term = teschenite}"

            an = self.An_value()
            if an is not None:
                if an <= 50.0:
                    if self.maf1 < 30.0:
                        name = "(Leuco-) " + self.foid_type().lower() + " diorite"
                    elif 30.0 <= self.maf1 < 70.0:
                        name = self.foid_type() + " diorite"
                    else:
                        name = "(Mela-) " + self.foid_type().lower() + " diorite"
                else:
                    if self.maf1 < 30.0:
                        name = "(Leuco-) " + self.foid_type().lower() + " " + self.Gabbro_diagrams().lower()
                    elif 30.0 <= self.maf1 < 70.0:
                        name = self.foid_type() + " " + self.Gabbro_diagrams().lower()
                    else:
                        name = "(Mela-) " + self.foid_type().lower() + " " + self.Gabbro_diagrams().lower()
            else:
                self.DialogWindow('WARN',
                                  "Classification with lack of accuracy",
                                  "It's not possible to accurately classificate this rock if the average content of anorthite is not provided.")
                if self.maf1 < 30.0:
                    name = r"(Leuco-) foid diorite\gabbro"
                elif 30.0 <= self.maf1 < 70.0:
                    name = r"Foid diorite\gabbro"
                else:
                    name = r"(Mela-) foid diorite\gabbro"

            #come per il Field_13, anche qui dobbiamo fare dei confronti per alcuni nomi speciali: Teschenite(Analc. Gabbro) e Theralite(Neph. Gabbro) [con %An]
            if an is not None:
                if "Nepheline gabbro" in name:
                    name = name + note1
                elif "Analcime gabbro" in name:
                    name = name + note2
            #costrutto per evitare la comparsa del termine (Leuco-) Anorthosite che perde di significato
            if '(Leuco-)' and 'anorthosite' in name:
                name = name.replace('(Leuco-) ', '')


            return name

        #Foidolite
        def Field_15(self):
            if self.maf1 < 30.0:
                name = "(Leuco-) " + self.foid_type().lower()
                note_neph = "\t{special term = urtite}"
                note_leuc = "\t{special term = italite}"
            elif 30.0 <= self.maf1 < 70.0:
                name = self.foid_type()
                note_neph = "\t\t{special term = ijolite}"
                note_leuc = "\t\t{special term = fergusite}"
            else:
                name = "(Mela-) " + self.foid_type().lower()
                note_neph = "\t{special term = melteigite}"
                note_leuc = "\t{special term = missourite}"

            if "nosean" in name.lower():
                name = name + "olite"
            elif "nepheline" in name.lower():
                name = name[:-1] + "olite" + note_neph
            elif "leucite" in name.lower():
                name = name[:-1] + "olite" + note_leuc
            else:
                name = name[:-1] + "olite"

            return name

#DEF PLAY-----------------------------------------------------------------(Algoritmo di calcolo)-----------------------------------------------------------------------

        def play(self):
            if self.maf2 >= 90.0:
                self.DialogWindow('CRIT',
                                  "Index Error",
                                  "Unacceptable percentage of M'', this may not be a plutonic rock.")

            elif self.qtz > 0.0 and self.foid > 0.0:                            # Easter egg
                self.DialogWindow('CRIT',
                                  "Unexpected error!",
                                  "Somehow you inserted both Q and F! I'm not programmed to classificate a rock that contains both foids and quartz.")

            elif self.qtz + self.kfel + self.pl + self.foid < 10.0:             # Scelta di utilizzo dei diagrammi per le rocce ultramafiche
                use_ultramafic_diagram = QW.QMessageBox.question(self,
                                                                    "Ultramafic rock",
                                                                    "This is an ultramafic rock. Do you want to use the ultramafic rocks diagrams?",
                                                                    QW.QMessageBox.Yes | QW.QMessageBox.No,
                                                                    QW.QMessageBox.No)
                if use_ultramafic_diagram == QW.QMessageBox.No:
                    self.resultShow.append("\nUltramafic rock (not specified)")
                    self.clearCanvas(self.ax1, self.canvas1)
                    self.clearCanvas(self.ax2, self.canvas2)
                else:
                    self.resultShow.append('\n' + self.ultramafic_rock())

            else:
                qtz_ric = (self.qtz*100.0)/(self.qtz + self.kfel + self.pl + self.foid)
                kfel_ric = (self.kfel*100.0)/(self.qtz + self.kfel + self.pl + self.foid)
                pl_ric = (self.pl*100.0)/(self.qtz + self.kfel + self.pl + self.foid)
                foid_ric = (self.foid*100.0)/(self.qtz + self.kfel + self.pl + self.foid)

                try:
                    pl_ratio = (pl_ric*100)/(kfel_ric+pl_ric)
                except ZeroDivisionError:                                       # Se il denominatore e' 0 non mi serira' il plagioclase ratio (i.e. 100% di Q o F)
                    pl_ratio = 0 # unused

                note = ""

                #vertici QAP
                if self.foid == 0.0:

                    self.drawPlot(PQA_plot, [(pl_ric, qtz_ric, kfel_ric)])

                    #Field 1a
                    if qtz_ric > 90.5:
                        name = self.Field_1a()

                    #Field 1b
                    elif 60.5 < qtz_ric <= 90.5:
                        name = self.Field_1b()

                    elif 20.5 < qtz_ric <= 60.5:

                        #Field 2
                        if pl_ratio <= 10.5:
                            name = self.Field_2()

                        #Field 3a
                        elif 10.5 < pl_ratio <= 35.5:
                            name = self.Field_3a()

                        #Field 3b
                        elif 35.5 < pl_ratio <= 65.5:
                            name = self.Field_3b()

                        #Field 4
                        elif 65.5 < pl_ratio <= 90.5:
                            name, note = self.Field_4()

                        #Field 5
                        else:
                            name = self.Field_5()

                    elif 5.5 < qtz_ric <= 20.5:

                        #Field 6Q
                        if pl_ratio <= 10.5:
                            name = self.Field_6Q()

                        #Field 7Q
                        elif 10.5 < pl_ratio <= 35.5:
                            name = self.Field_7Q()

                        #Field 8Q
                        elif 35.5 < pl_ratio <= 65.5:
                            name = self.Field_8Q()

                        #Field 9Q
                        elif 65.5 < pl_ratio <= 90.5:
                            name = self.Field_9Q()

                        #Field 10Q
                        else:
                            name = self.Field_10Q()

                    else:

                        #Field 6
                        if pl_ratio <= 10.5:
                            name = self.Field_6()

                        #Field 7
                        elif 10.5 < pl_ratio <= 35.5:
                            name = self.Field_7()

                        #Field 8
                        elif 35.5 < pl_ratio <= 65.5:
                            name = self.Field_8()

                        #Field 9
                        elif 65.5 < pl_ratio <= 90.5:
                            name = self.Field_9()

                        #Field 10
                        else:
                            name = self.Field_10()


                #vertici APF
                else:

                    self.drawPlot(PFA_plot, [(pl_ric, foid_ric, kfel_ric)])

                    #Field 15
                    if foid_ric > 60.5:
                        name = self.Field_15()

                    elif 10.5 < foid_ric <= 60.5:

                        #Field 11
                        if pl_ratio <= 10.5:
                            name = self.Field_11()

                        #Field 12
                        elif 10.5 < pl_ratio <= 50.5:
                            name, note = self.Field_12()

                        #Field 13
                        elif 50.5 < pl_ratio <= 90.5:
                            name = self.Field_13()

                        #Field 14
                        else:
                            name = self.Field_14()

                    else:

                        #Field 6F
                        if pl_ratio <= 10.5:
                            name, note = self.Field_6F()

                        #Field 7F
                        elif 10.5 < pl_ratio <= 35.5:
                            name  = self.Field_7F()

                        #Field 8F
                        elif 35.5 < pl_ratio <= 65.5:
                            name = self.Field_8F()

                        #Field 9F
                        elif 65.5 < pl_ratio <= 90.5:
                            name = self.Field_9F()

                        #Field 10F
                        else:
                            name = self.Field_10F()


                if not name.startswith('('):
                    name = name.capitalize()
                self.resultShow.append('\n' + name)

                if note != "":
                    self.DialogWindow('INFO', "Note(s)", note)

#DEF Costruttori------------------------------------------------------------------(PYQT4)------------------------------------------------------------------------------

        def toggleTicks(self, state):

            if state:
                self.plotTicks = True
            else:
                self.plotTicks = False


        def toggleGrid(self, state):

            if state:
                self.plotGrid = True
            else:
                self.plotGrid = False


        def clearCanvas(self, axes, canvas):

            axes.cla()
            axes.axis('off')
            canvas.draw_idle()


        def drawPlot(self, diagram, points, mainPlot=True):

            ''' Function to generete the final plot.
                diagram = Name of the plot function.
                points = List of 3-tuple(x, y, z). Points plotted on plot.
                mainPlot = If True the result will be plotted on first canvas.
            '''

            if mainPlot:
                self.clearCanvas(self.ax1, self.canvas1)
                self.clearCanvas(self.ax2, self.canvas2)
                canvas = self.canvas1
                ax = self.ax1

            else:
                canvas = self.canvas2
                ax = self.ax2

            if self.Image:
                # Create Ternary Diagram background
                fig, tax = diagram(ax, self.plotGrid, self.plotTicks)
                # Plot points of data
                tax.scatter(points, color='red')
                # Remove default Matplotlib ticks
                tax.clear_matplotlib_ticks()
                # Adjust figure
                fig.tight_layout()
                # Draw figure on canvas
                canvas.draw()


        def open_file(self):

            fName, _ = QW.QFileDialog.getOpenFileName(
                self, "Import from text file", "", self.tr("Text Files (*txt)"))

            try:
                print(fName)
                f = open(fName, 'r', encoding='utf-8')

            except (IOError, PermissionError):
                f = False

            if f:
                self.clear_values()
                try:
                    num = 1                                                     # Serve a saltare la riga dei titoli
                    dictionary = {}
                    tot_count = 0
                    for x in f.readlines():
                        if num == 1:                                            # Serve a saltare la riga dei titoli
                            num += 1
                        count, mineral = x.replace('\n','').split(';')[-2:]     # Prendo solo 'count' e 'mineral' che sono gli elementi che mi interessano
                        count = float(int(count))
                        dictionary[mineral] = count                             # Inserisco i valori accoppiati nel dizionario
                        tot_count += count                                      # Creo la somma dei count (serve per la percentuale)


                    for key, value in dictionary.items():
                        mineral_percentage = round((value*100)/tot_count, 1)    # Trasformiamo i count (qui espressi come values del dizionario) in percentuali

                        if key == 'Q':
                            self.Q_Label.setText(str(mineral_percentage) + '%')
                            self.qtz = mineral_percentage
                        elif key == 'A':
                            self.A_Label.setText(str(mineral_percentage) + '%')
                            self.kfel = mineral_percentage
                        elif key == 'P':
                            self.P_Label.setText(str(mineral_percentage) + '%')
                            self.pl = mineral_percentage
                        elif key == 'F':
                            self.F_Label.setText(str(mineral_percentage) + '%')
                            self.foid = mineral_percentage
                        elif key == "M'":
                            self.M1_Label.setText(str(mineral_percentage) + '%')
                            self.maf1 = mineral_percentage
                        elif key == 'M"' or key == "M''":                       # Gli utenti potrebbero scriverlo in due modi diversi
                            self.M2_Label.setText(str(mineral_percentage) + '%')
                            self.maf2 = mineral_percentage

                except ValueError:
                    self.DialogWindow('CRIT',
                                      "File not compatible",
                                      "The text file you've selected is not compatible")

                self.update_tot()
                f.close()


        def triangle_choice(self, text):

            if text == "Q-A-P":
                self.triangleChoice = "QAP"
                self.F_Label.setText("0.0%")
                self.foid = 0
                self.update_tot()
            else:
                self.triangleChoice = "APF"
                self.Q_Label.setText("0.0%")
                self.qtz = 0
                self.update_tot()


        def active_images(self, state):

            # states --> 0 = unchecked, 1 = partially checked, 2 = checked
            self.Image = state == 2


        def Q_insertValue(self):

            if self.triangleChoice == "APF":
                Q_max = 0
            else:
                Q_max = 100

            qtz, ok = QW.QInputDialog.getDouble(self, "Q",
                                                   self.tr("Amount:"),
                                                   self.qtz, 0, Q_max, 1)
            if ok:
                self.Q_Label.setText(str(qtz)+"%")
                self.qtz = qtz
                self.update_tot()


        def A_insertValue(self):

            kfel, ok = QW.QInputDialog.getDouble(self, "A",
                                                    self.tr("Amount:"),
                                                    self.kfel, 0, 100, 1)
            if ok:
                self.A_Label.setText(str(kfel)+"%")
                self.kfel = kfel
                self.update_tot()


        def P_insertValue(self):

            pl, ok = QW.QInputDialog.getDouble(self, "P",
                                                  self.tr("Amount:"),
                                                  self.pl, 0, 100, 1)
            if ok:
                self.P_Label.setText(str(pl)+"%")
                self.pl = pl
                self.update_tot()


        def F_insertValue(self):

            if self.triangleChoice == "QAP":
                F_max = 0
            else:
                F_max = 100

            foid, ok = QW.QInputDialog.getDouble(self, "F",
                                                    self.tr("Amount:"),
                                                    self.foid, 0, F_max, 1)
            if ok:
                self.F_Label.setText(str(foid)+"%")
                self.foid = foid
                self.update_tot()


        def M1_insertValue(self):

            maf1, ok = QW.QInputDialog.getDouble(self, "M'",
                                                    self.tr("Amount:"),
                                                    self.maf1, 0, 100, 1)
            if ok:
                self.M1_Label.setText(str(maf1)+"%")
                self.maf1 = maf1
                self.update_tot()


        def M2_insertValue(self):

            maf2, ok = QW.QInputDialog.getDouble(self, "M''",
                                                    self.tr("Amount:"),
                                                    self.maf2, 0, 100, 1)
            if ok:
                self.M2_Label.setText(str(maf2)+"%")
                self.maf2 = maf2
                self.update_tot()


        def start_classification(self):

            # Il round serve ad evitare i problemi con l'input di testo
            if round(self.qtz + self.kfel + self.pl + self.foid + self.maf1 + self.maf2, 1) == 100.0:
                self.play()
            else:
                self.DialogWindow('WARN',
                                  "Index Error",
                                  "Check your indices: their sum shouldn't be higher or lower than 100.0%")


        def update_tot(self):

            tot = str(self.qtz + self.kfel + self.pl + self.foid + self.maf1 + self.maf2)
            self.tot_Label.setText("Total: {}% / 100.0%".format(tot))
            if float(tot) == 100.0:
                self.tot_Label.setStyleSheet('color: green')
            else:
                self.tot_Label.setStyleSheet('color: red')


        def DialogWindow(self, msgType, title, text):

            typedict = {'INFO' : QW.QMessageBox.information,
                        'WARN' : QW.QMessageBox.warning,
                        'CRIT' : QW.QMessageBox.critical}
            typedict[msgType](self, title, text)


        def show_guideIT(self):

            guide = "Per classificare una roccia plutonica, segui questi step:\n\n\n\
(1)\nScegli quale delle due meta' del diagramma QAPF vuoi usare (Q-A-P o A-P-F) tramite il menu a tendina situato nella parte sinista della finestra.\n\n\
(2)\nSeleziona la percentuale modale (NON ricalcolata a 100) di quarzo/feldspatoide, alkali-feldspato, plagioclasio, minerali mafici (ed associati) \
colorati (M') ed incolori (M''), utilizzando i bottoni situati nella parte destra della finestra.\n\n\
(3)\nCombina tutte le percentuali finche' la scritta situata in basso a destra non diventa verde (cio' significa che la somma di tutte le percentuali e' \
esattamente 100%).\n\n\
(4)\nClicca il bottone 'START'.\n\n\
(5)\nInserisci altre informazioni opzionali se il programma le richiede (in certi casi potrebbero apparire delle finestre aggiuntive).\n\n\
(6)\nIl nome della roccia risultante sara' mostrato nella parte inferiore della finestra (puoi cambiare sia il colore che il font dal menu 'Edit').\n\n\
(7)\nSe la casella 'Display Diagram' e' spuntata, l'interpretazione grafica del risultato verra' raffigurata all'interno delle due aree di proiezione \
situate nella parte superiore della finestra. L'area di sinistra conterra' il diagramma QAPF, mentre quella di destra conterra' i diagrammi delle rocce \
ultramafiche o gabbroiche quando necessari.\n\n\n\
Buon lavoro!"

            self.DialogWindow('INFO', "Guida", guide)


        def show_guideEN(self):

            guide = "Follow these steps to classify a plutonic rock:\n\n\n\
(1)\nChoose which of the two QAPF triangular diagram you want to use (Q-A-P or A-P-F), using the drop-down menu located on the left side of the window.\n\n\
(2)\nSelect the modal percentage (NOT recalculated to 100) of quartz/foid, alkali-feldspar, plagioclase, coloured (M') and colourless (M'') mafic and \
related minerals, using the buttons located on the right side of the window.\n\n\
(3)\nCombine all the percentages until the down-right located label turns green (this means that the sum of all percentages is exactly 100%).\n\n\
(4)\nClick on 'START' button.\n\n\
(5)\nEnter other optional information if the program requires it (pop-up windows may occasionally appear).\n\n\
(6)\nThe resulting rock name will be displayed in the lower part of the window (you can either change the color or the font from the 'Edit' menu).\n\n\
(7)\nIf the 'Display Diagram' checkbox is checked, the graphic interpretation of the result will be shown within the two plotting areas located in the \
upper side of the window. The left plotting area will hold the QAPF diagram, while the right one will contain ultramafic or gabbroic rocks diagrams when \
they are required.\n\n\n\
Enjoy the tool!"

            self.DialogWindow('INFO',"Guide", guide)


        def clear_values(self):

            self.Q_Label.setText("0.0%")
            self.qtz = 0
            self.A_Label.setText("0.0%")
            self.kfel = 0
            self.P_Label.setText("0.0%")
            self.pl = 0
            self.F_Label.setText("0.0%")
            self.foid = 0
            self.M1_Label.setText("0.0%")
            self.maf1 = 0
            self.M2_Label.setText("0.0%")
            self.maf2 = 0
            self.update_tot()


        def change_color(self):

            color = QW.QColorDialog.getColor(QG.QColor(0, 0, 255), self)
            if color.isValid():
                self.resultShow.setTextColor(color)


        def change_font(self):

            font, ok = QW.QFontDialog.getFont()
            if ok:
                self.resultShow.setFont(font)


        def clear_history(self):

            choice = QW.QMessageBox.question(self, "Clear confirm",
                                                "Do you really want to clear the history?",
                                                QW.QMessageBox.Yes | QW.QMessageBox.No,
                                                QW.QMessageBox.No)
            if choice == QW.QMessageBox.Yes:
                self.resultShow.clear()


        def close_application(self):

            choice = QW.QMessageBox.question(self, "Exit confirm",
                                                "Do you want to close the program?",
                                                QW.QMessageBox.Yes | QW.QMessageBox.No,
                                                QW.QMessageBox.No)
            if choice == QW.QMessageBox.Yes:
                sys.exit(app.exec_())


        def closeEvent(self, a0):

            if a0:
                a0.ignore()
            self.close_application()


if __name__ == "__main__":
    app = QW.QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())