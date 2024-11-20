from qgis.core import QgsMapSettings, QgsMapRendererParallelJob, QgsProject, Qgis  # Ajout de Qgis ici
from qgis.PyQt.QtWidgets import QAction, QFileDialog
from qgis.PyQt.QtGui import QImage, QPainter
from qgis.PyQt.QtCore import QSize, Qt
from qgis.utils import iface

class CaptureCartePlugin:
    def __init__(self, iface):
        """Initialisation du plugin"""
        self.iface = iface
        self.action = None

    def initGui(self):
        """Initialisation de l'interface utilisateur du plugin"""
        self.action = QAction("Capture de carte", self.iface.mainWindow())
        self.action.triggered.connect(self.capture_map)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Capture Carte Plugin", self.action)

    def unload(self):
        """Nettoyage du plugin à la fermeture"""
        self.iface.removeToolBarIcon(self.action)
        self.iface.removePluginMenu("&Capture Carte Plugin", self.action)

    def capture_map(self):
        """Méthode pour capturer la carte"""
        output_path, _ = QFileDialog.getSaveFileName(self.iface.mainWindow(), "Enregistrer la capture d'écran", "", "PNG Files (*.png);;JPEG Files (*.jpg)")
        if not output_path:
            return

        # Configurer les paramètres de la carte
        map_settings = QgsMapSettings()
        map_settings.setLayers([layer for layer in QgsProject.instance().mapLayers().values()])
        map_settings.setBackgroundColor(Qt.white)
        map_settings.setOutputSize(QSize(1920, 1080))  # Dimensions de l'image
        map_settings.setOutputDpi(300)  # Augmente la qualité de l'image
        map_settings.setExtent(self.iface.mapCanvas().extent())  # Utilise l'étendue actuelle de la carte
        map_settings.setDestinationCrs(QgsProject.instance().crs())  # Définit le système de coordonnées de destination

        # Créer une tâche de rendu pour la carte
        job = QgsMapRendererParallelJob(map_settings)
        job.start()
        job.waitForFinished()

        # Obtenir l'image rendue
        image = job.renderedImage()
        
        if image:
            # Sauvegarder l'image en fonction du format choisi
            format_extension = "JPEG" if output_path.endswith(".jpg") else "PNG"
            image.save(output_path, format_extension)
            self.iface.messageBar().pushMessage("Succès", "La capture d'écran de la carte a été sauvegardée.", level=Qgis.Info)
        else:
            self.iface.messageBar().pushMessage("Erreur", "Impossible de capturer l'image.", level=Qgis.Critical)
