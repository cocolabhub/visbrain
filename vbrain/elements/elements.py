import vispy.visuals.transforms as vist
from vispy.scene import Node

from .AtlasBase import AtlasBase
from .SourcesBase import SourcesBase
from .ConnectivityBase import ConnectivityBase
from .CmapBase import CmapBase
from .transformations import transformations

class elements(CmapBase, transformations):

    """docstring for elements
    """

    def __init__(self, canvas, progressbar, **kwargs):
        # Initialize transformation with Null:
        self.transform = vist.ChainTransform([vist.NullTransform()])
        self.progressbar = progressbar

        # Initialize brain, sources and connectivity elements :
        self.atlas = AtlasBase(a_transform=self.transform, **kwargs)
        self.sources = SourcesBase(s_transform=self.atlas.transform, **kwargs)
        self.connect = ConnectivityBase(c_transform=self.atlas.transform, c_xyz=self.sources.xyz, **kwargs)
        CmapBase.__init__(self, **kwargs)

        # Add transformations :
        transformations.__init__(self, **kwargs)

        # Manage visible panel :
        if self.sources.xyz is None:
            self.q_SOURCES.setEnabled(False)
            self.menuTransform.setEnabled(False)
            self.q_TRANS.setEnabled(False)
            self.q_CONNECT.setEnabled(False)
            self.o_Sources.setEnabled(False)
            self.o_Text.setEnabled(False)
        if self.connect.connect is None:
            self.q_CONNECT.setEnabled(False)
            self.o_Connect.setEnabled(False)

        # Update slider with the brain opacity:
        self.OpacitySlider.setValue(self.atlas.opacity*100)

        self._vbNode = Node(name='visbrain')
        self.atlas.mesh.parent = self._vbNode
        self.sources.mesh.parent = self._vbNode
        self.connect.mesh.parent = self._vbNode
        self.sources.stextmesh.parent = self._vbNode
