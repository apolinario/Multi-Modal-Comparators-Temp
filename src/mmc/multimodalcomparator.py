# this should probably be a nn.Module
#class MultiModalComparator(nn.Module):
class MultiModalComparator:
    """
    Generic class for encapsulating models that can compare data across multiple modalities
    """
    def __init__(self,
        name=None,
        #modalities=[TEXT]
        device=DEVICE,
    ):
        self.modes = {}
        self.device=device
        #for m in modalities:
        #  self.register_modality(m)
        #assert len(self.modes) > 0

    def register_modality(
        self, 
        modality,
        projector,
        preprocessor=None,
        postprocessor=None,
    ):
        """
        Register a modality with this MMC. 
        
        The MMC class (this) will manage how data from this modality is processed 
        for performing comparisons with other modalities supported by this MMC.
        This registration function specifies that procedure for a single modality.

        An MMC is required to have a single processing procedure for each modality it
        supports. If data for a modality can be read in from different formats, that should
        be addressed by the Modality class. If your given modality requires different processing
        procedures, you may need to revisit how you are defining "modalities" here. For example,
        the CARP model compares passages of narrative text to criticisms of the passages. Although
        both the passages and criticisms are "text", from the perspective of CARP they are
        separate modalities. To implement a CARP-like model, you would first create PASSAGE and 
        CRITIQUE modalities (subclassing from the TEXT modality), and then you could register
        the appropriate processing procedures for those modalities separately here.
        """
        assert modality.name not in self.modes
        #if preprocessor is not None:
        #  preprocessor.to(self.device)
        #if postprocessor is not None:
        #  postprocessor.to(self.device)
        if preprocessor is None: 
            preprocessor = lambda x: x # could lambdas cause pickling issues? 
        if postprocessor is None:
            postprocessor = lambda x: x
        self.modes[modality.name] = {
            'modality_obj':modality,
            'projector':projector, #.to(self.device),
            'preprocessor':preprocessor,
            'postprocessor':postprocessor,
        }
    def supports_modality(self, modality):
        return modality.name in self.modes

    def _supports_mode(self, modality_name):
       return modality_name in self.modes

    def _project_item(self, item, mode):
        assert self._supports_mode(mode)
        project = self.modes[mode]['projector']
        preprocess = self.modes[mode]['preprocessor']
        item = preprocess(item)
        item.to(self.device)
        return project(item)

    @property
    def supports_text(self):
       return self._supports_mode('text')
    @property
    def supports_image(self):
        return self._supports_mode('image')
    @property
    def supports_audio(self):
        return self._supports_mode('audio')  

    def project_text(self, text):
        return self._project_item(text, 'text')
    def project_image(self, image):
        return self._project_item(image, 'image')
    def project_audio(self, audio):
       return self._project_item(audio, 'audio')
    @property
    def name(self):
       return str(self)
