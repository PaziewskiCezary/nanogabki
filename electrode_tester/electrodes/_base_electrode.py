from dataclasses import dataclass, field
from typing import Union, Dict, Tuple, List, Iterable

@dataclass(init=True, repr=True, frozen=True)
class BaseElectrode:
    electrode_type: str = field(repr=False)
    salt_type: str
    salty_value: Union[float, int] # as %
    normal_height: Union[float, int] # cm
    squeeze_height: Union[float, int] # cm
    
    width: Union[float, int] # cm
    height_delta: Union[float, int] # cm 
    normal_height_var: Union[float, int] # cm

    _available_electrode_types = ['vileda', 'nano', 'white sponge', 'gel']
    _available_salt_types = ['saline', 'custom', 'tap solution', 'distilled water solution', 'n/a']

    def __post_init__(self):

        self._check_electrode_type(self.electrode_type)
        self._check_salt_type(self.salt_type)
        self._check_salty_value(self.salty_value)
        self._check_squeeze_height(self.squeeze_height)
        
        self._check_value(self.normal_height, 'normal_height')
        self._check_value(self.width, 'width')
        self._check_value(self.height_delta, 'height_delta')
        self._check_value(self.normal_height_var, 'normal_height_var')
        
        
    def __lt__(self, other):
        if not isinstance(other, BaseElectrode):
            raise ValueError('Can compare only with other "BaseElectrode" class instance')

        return (self.electrode_type, self.salt_type, self.salty_value, self.height) < (other.electrode_type, other.salt_type, other.salty_value, other.height)

    def _check_electrode_type(self, electrode:str):
        if not isinstance(electrode, str):
            raise ValueError(f'"electrode_type" should be "string" from '\
                             f'`available_electrode_types` not {electrode}')
        electrode = electrode.lower().strip()
        if electrode not in self._available_electrode_types:
            raise ValueError(f'"electrode_type" should be one of '\
                             f'`available_electrode_types` not {electrode}')

    def _check_salt_type(self, salt:str):
        if not isinstance(salt, str):
            raise ValueError(f'"salt_type" should be "string" from '\
                             f'`available_salt_types` not {salt}')
        salt = salt.lower().strip()
        if salt not in self._available_salt_types:
            raise ValueError(f'"salt_type" should be one of '\
                             f'`available_salt_types` not {salt}')

    def _check_salty_value(self, value:float):
        if not isinstance(value, (float, int) ) or not (0 <= value <= 100 or value != float("nan")):
            raise ValueError(f'"salty_value" should be "float" or "integer" '\
                             f'between 0 and 100 or "nan", not "{value}"')

    def _check_squeeze_height(self, valule:Union[float, int]):
        if not isinstance(valule, (float, int)) or valule < 0:
            raise ValueError(f'"{name}" should be no negative "integer" or "flaot" not bigger than normal_height={self.normal_height}, not "{valule}"')
            
    def _check_value(self, valule:Union[float, int], name):
        if not isinstance(valule, (float, int)) or valule <= 0:
            raise ValueError(f'"{name}" should be positive "integer" or "flaot", not "{valule}"')

    def height(self):
        raise NotImplemented
    
    def height_error(self):
        raise NotImplemented
        