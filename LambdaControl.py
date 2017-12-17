from __future__ import with_statement #compatibility for Live 9, need to be written at the first line of the script
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.InputControlElement import *
from _Framework.SessionComponent import SessionComponent     #this is the component used to create Sessions
from _Framework.Layer import Layer

from ConfigurableButtonElement import ConfigurableButtonElement
from SkinDefault import make_default_skin

import Colors

NUMBER_OF_TRACKS = 10
NUMBER_OF_SCENES = 6

TRACK_OFFSET   = 0
SCENE_OFFSET   = 0

#MIDI channel for the matrix
MATRIX_CHANNEL = 0
PAD_OFFSET = 36 # for first note

#navigation controls
MATRIX_CONTROL_CHN = 2
MATRIX_CONTROL_KEY_UP = 0
MATRIX_CONTROL_KEY_DOWN = 1
STOP_ALL_CLIPS_CHN = 2
STOP_ALL_CLIPS_KEY = 24

STOP_TRACK_CLIP_OFFSET = 102

class LambdaControl(ControlSurface):
    __module__=__name__
    __doc__="LambdaControl Live Script"

    def __init__(self, c_instance):
        ControlSurface.__init__(self,c_instance)
        with self.component_guard():
            self.__c_instance = c_instance
            self._skin = make_default_skin()

            #scene up and down by encoder
            self.pad_down_button = self.create_button(MATRIX_CONTROL_CHN, MATRIX_CONTROL_KEY_DOWN, MIDI_NOTE_TYPE, 'Down_Button', is_rgb=False)
            self.pad_up_button = self.create_button(MATRIX_CONTROL_CHN, MATRIX_CONTROL_KEY_UP, MIDI_NOTE_TYPE, 'Up_Button', is_rgb=False)

            #stop all clips by press on switch scene encoder
            self.stop_all_clips_button = self.create_button(STOP_ALL_CLIPS_CHN, STOP_ALL_CLIPS_KEY, MIDI_NOTE_TYPE, 'Stop_All_Clips_Button', is_rgb=False)

            #array for stop track clip buttons
            self.stop_track_clip_buttons_raw = [[ self.create_button(MATRIX_CHANNEL, STOP_TRACK_CLIP_OFFSET + i, MIDI_CC_TYPE,
                                                                     'Stop_' + str(i) + '_Button', is_rgb=True) for i in range(NUMBER_OF_TRACKS) ]]
            self.stop_track_clip_buttons = ButtonMatrixElement(name='Stop_Track_Clip_Buttons', rows=self.stop_track_clip_buttons_raw)

            self.matrix_rows_raw = [[ self.create_button(MATRIX_CHANNEL, (NUMBER_OF_SCENES - 1 - row) * NUMBER_OF_TRACKS + column + PAD_OFFSET,
                                                         MIDI_NOTE_TYPE, str(column) + '_Clip_' + str(row) + '_Button', is_rgb=True,
                                                         default_states={True: 'DefaultMatrix.On', False: 'DefaultMatrix.Off'}) for column in xrange(NUMBER_OF_TRACKS) ]
                                      for row in xrange(NUMBER_OF_SCENES) ]
            self.matrix = ButtonMatrixElement(name='Button_Matrix', rows=self.matrix_rows_raw)
            self.side_buttons = ButtonMatrixElement(name='Scene_Launch_Buttons',
                                                    rows=[[ self.create_button(MATRIX_CHANNEL, 36 + idx, MIDI_CC_TYPE, 'Scene_Launch_Button' + str(idx),
                                                    is_rgb=True, default_states={True: 'DefaultMatrix.On', False: 'DefaultMatrix.Off'}) \
                                for idx in reversed(xrange(NUMBER_OF_SCENES)) ]])

            #initialisation of the session
            self.create_session()
            self.set_highlighting_session_component(self.session)

    def create_button(self, channel, note, midi_type, name, **k):
        return ConfigurableButtonElement(True, midi_type, channel, note, name=name, skin=self._skin, **k)

    def create_session_layer(self):
        return Layer(scene_launch_buttons=self.side_buttons, clip_launch_buttons=self.matrix,
                     stop_track_clip_buttons=self.stop_track_clip_buttons, stop_all_clips_button=self.stop_all_clips_button,
                     scene_bank_up_button=self.pad_up_button, scene_bank_down_button=self.pad_down_button)

    def create_session(self):
        self.session = SessionComponent(NUMBER_OF_TRACKS, NUMBER_OF_SCENES, enable_skinning=True,
                                        is_enabled=False, auto_name=True, layer=self.create_session_layer())
        self.session.set_offsets(TRACK_OFFSET, SCENE_OFFSET) #offset start a the up-left corner (track1,row1)
        self.session._do_show_highlight()   #to ensure that this session will be highlighted
        self.session.set_rgb_mode(Colors.CLIP_COLOR_TABLE, Colors.RGB_COLOR_TABLE, clip_slots_only=True)
        self.session.set_enabled(True)

    def get_matrix_button(self, column, row):
        return self.matrix_rows_raw[NUMBER_OF_SCENES - row][column]
