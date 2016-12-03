import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def save_fig(fig, figName, fmt=".all"):
    if fmt == ".pdf":
        pdf = PdfPages(figName + format)
        pdf.savefig(fig)
        pdf.close()
    elif fmt == ".all":
        pdf = PdfPages(figName + ".pdf")
        pdf.savefig(fig)
        pdf.close()
        plt.savefig(figName + ".png")
        plt.savefig(figName + ".jpg")
    else:
        plt.savefig(figName + fmt)