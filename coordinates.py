#!/usr/bin/env python3
"""
Get the coordinates to put the postcard to the door.
"""
# pylint: disable=[logging-fstring-interpolation]
from argparse import ArgumentParser
from pathlib import Path
from enum import Enum
from math import sqrt, atan, pi
from random import seed, randint, randrange, choice
import logging


seed()


BUSY_FILE = Path(__file__).parent / 'busy.csv'


UNITS: dict[str, dict[str, float]] = {
    'length': {
        # name: factor = mm in unit
        'mm': 1.0,
        'light-year': 9.4607e18,
        'astronomical unit': 149597870700000.0,
        'parsec': 3.0857e19,

        # Unusual
        'horizontal pitch': 5.08,
        'hammer unit': 19.05,
        'rack U': 44.45,
        'light-ns': 299.792,
        'metric foot': 300.0,
        'horse': 2400.0,
        'boat': 19000.0,
        'Manhattan block': 80000.0,
        'Earth radius': 6371000000.0,
        'Siriometer': 149.6e18,

        # Humorous
        'Altuve': 1650.0,
        'Attoparsec': 30.86,
        'Beard-second': 10e-6,
        'Sheppey': 1400000.0,
        'Smoot': 1700.0,

        # English
        'line': 2.12,
        'barleycorn': 8.47,
        'digit': 19.05,
        'finger': 22.23,
        'inch': 25.4,
        'nail': 57.15,
        'palm': 76.2,
        'hand': 101.6,
        'foot': 304.8,
        'cubit': 457.2,
        'yard': 914.0,
        'ell': 1143.0,
        'fathom': 1829.0,
        'rod': 5000.0,
        'chain': 20116.0,
        'furlong': 2011680.0,
        'mile': 1610000.0,
        'NM': 1852000.0,
        'league': 4830000.0,
    },

    'angle': {
        # name: factor equals half a turn
        'rad': 0,  # means "do nothing"
        'degree': 180.0,
        'arcminute': 10800.0,
        'arcsecond': 1296000.0 / 2.0,
        'grad': 200.0,
        'hour angle': 12.0,
        'compass point': 16.0,
        'binary degree': 128.0,
        'quadrant': 2.0,
        'sextant': 3.0,
        'hexacontade': 30.0,
        'diameter part': 376.991 / 2.0,
        'zam': 112.0,
        'Akhnam': 16.0,
    },
}


class Orientation(Enum):
    """ Orientation for the postcard """
    UNDEFINED = 0
    LANDSCAPE = 1
    PORTRAIT = 2


class Rectangle:
    """
    2-dimensional object.
    """
    def __init__(self, xxx: int, zzz: int, width: int, height: int) -> None:
        self.xxx = xxx
        self.zzz = zzz
        self.width = width
        self.height = height

        self._logger = logging.getLogger(self.__class__.__name__)

    def __repr__(self) -> str:
        return (
            f'<{self.__class__.__name__}: '
            f'x=({self.xxx:4}, {self.xxx + self.width:4}) '
            f'z=({self.zzz:4}, {self.zzz + self.height:4})'
            '>'
        )

    def overlap(self, other: 'Rectangle') -> bool:
        """
        Test if there is an overlap with the other object.
        """
        x_11 = self.xxx > other.xxx
        x_12 = self.xxx < other.xxx + other.width
        x_21 = self.xxx + self.width > other.xxx
        x_22 = self.xxx + self.width < other.xxx + other.width
        x_test = (x_11 and x_12) or (x_21 and x_22)

        z_11 = self.zzz > other.zzz
        z_12 = self.zzz < other.zzz + other.height
        z_21 = self.zzz + self.height > other.zzz
        z_22 = self.zzz + self.height < other.zzz + other.height
        z_test = (z_11 and z_12) or (z_21 and z_22)

        self._logger.info(
            f' overlap {self} vs {other} -> '
            f'x={int(x_test)}=({int(x_11)} and {int(x_12)}) or ({int(x_21)} and {int(x_22)})'
            ' AND '
            f'z={int(z_test)}=({int(z_11)} and {int(z_12)}) or ({int(z_21)} and {int(z_22)})'
        )

        return x_test and z_test

    def overflow(self, other: 'Rectangle') -> bool:
        """
        Test if there is an overflow of self compared to other (no total overlap).
        """
        x_test = self.xxx < other.xxx or self.xxx + self.width > other.xxx + other.width
        z_test = self.zzz < other.zzz or self.zzz + self.height > other.zzz + other.height

        self._logger.info(f'overflow {self} vs {other}: {x_test=} or {z_test=}')

        return x_test or z_test

    def get_cartesian(self) -> tuple:
        """ Get coordinates in Cartesian notation. """
        return (self.xxx, self.zzz)

    def get_polar(self) -> tuple:
        """ Get coordinates in polar notation. """
        return (
            sqrt(self.xxx**2 + self.zzz**2),
            atan(self.zzz / self.xxx)
        )

    def get_str_coordinates(self) -> str:
        """ Get coordinates. """
        coordinate_system = randrange(2)

        if coordinate_system == 0:
            # cartesian
            cartesian_coord = list(self.get_cartesian())

            x_name, x_factor = choice(list(UNITS['length'].items()))
            y_name, y_factor = choice(list(UNITS['length'].items()))

            cartesian_coord[0] /= x_factor
            cartesian_coord[1] /= y_factor

            return f'(x = {cartesian_coord[0]} {x_name}, y = {cartesian_coord[1]} {y_name})'

        if coordinate_system == 1:
            polar_coord = list(self.get_polar())

            r_name, r_factor = choice(list(UNITS['length'].items()))
            phi_name, phi_factor = choice(list(UNITS['angle'].items()))

            polar_coord[0] /= r_factor

            if phi_factor != 0:
                polar_coord[1] *= (phi_factor / pi)

            return f'(r = {polar_coord[0]} {r_name}, phi = {polar_coord[1]} {phi_name})'

        raise NotImplementedError(f'Unknown coordinate system: {coordinate_system}')


THE_DOOR = Rectangle(0, 0, 800, 2000)


class Postcard(Rectangle):
    """
    Postcard object.
    """
    WIDTH = 146  # [mm]
    HEIGHT = 106  # [mm]

    def __init__(self, xxx: int = None, zzz: int = None, orientation: Orientation = None):
        if orientation is Orientation.LANDSCAPE:
            width = self.WIDTH
            height = self.HEIGHT
        elif orientation is Orientation.PORTRAIT:
            width = self.HEIGHT
            height = self.WIDTH

        else:
            width = self.WIDTH
            height = self.WIDTH

        if xxx is None or zzz is None:
            if xxx is not None or zzz is not None:
                raise ValueError('Either provide both coordinates or none, cannot work with half.')

            xxx = randint(0, THE_DOOR.width - width)
            zzz = randint(0, THE_DOOR.height - height)

        super().__init__(xxx, zzz, width, height)

        if orientation is None:
            orientation = Orientation.UNDEFINED

        self.orientation = orientation

    def as_string(self) -> str:
        """ Get the postcard's coordinates as a string for use in CSV. """
        return f'{self.xxx},{self.zzz},{self.orientation.name}'

    @classmethod
    def from_string(cls, args: str) -> 'Postcard':
        """
        Create a new location object from a string from a CSV file.
        """
        xxx, zzz, orientation_str = args.split(',')
        return cls(int(xxx), int(zzz), Orientation[orientation_str])


def parse_busy() -> list[Postcard]:
    """
    Parse the file of busy locations.
    """
    contents = BUSY_FILE.read_text().splitlines()

    postcards = []
    for line in contents:
        if line.startswith('#'):
            continue

        postcards.append(Postcard.from_string(line))

    return postcards


def write_busy(postcards: list[Postcard]) -> None:
    """
    Write the busy location file.
    """
    contents = '# x,z,orientation\n'
    contents += '\n'.join(postcard.as_string() for postcard in postcards) + '\n'
    BUSY_FILE.write_text(contents)


def test_new(new_postcard: Postcard, postcards: list[Postcard]) -> bool:
    """
    Test if the new one is OK or not.
    """
    if new_postcard.overflow(THE_DOOR):
        return False

    for postcard in postcards:
        if new_postcard.overlap(postcard):
            return False

    return True


def main():
    """
    Main function called when this script is executed.
    """
    parser = ArgumentParser()

    parser.add_argument(
        '-v',
        '--verbose',
        action='count',
        default=0,
        help='Get more output from this script',
    )

    parser.add_argument(
        '-d',
        '--dryrun',
        action='store_true',
        default=False,
        help='Dry run: do not write the file.',
    )

    parser.add_argument(
        '-p',
        '--portrait',
        action='store_true',
        default=False,
        help='postcard is in portrait orientation',
    )

    parser.add_argument(
        '-l',
        '--landscape',
        action='store_true',
        default=False,
        help='postcard is in landscape orientation',
    )

    args = parser.parse_args()

    if not args.landscape and not args.portrait:
        raise ValueError('Please specify if it is landscape or portrait (no default)')

    orientation = Orientation.PORTRAIT if args.portrait else Orientation.LANDSCAPE

    log_levels = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
    if args.verbose is None:
        args.verbose = 0
    elif args.verbose >= len(log_levels):
        args.verbose = len(log_levels)

    logging.basicConfig(level=log_levels[args.verbose])

    existing_postcards = parse_busy()

    postcard = Postcard(orientation=orientation)
    while not test_new(postcard, existing_postcards):
        postcard = Postcard(orientation=orientation)

    existing_postcards.append(postcard)

    if not args.dryrun:
        write_busy(existing_postcards)

    print(f'coordinates: {postcard.get_str_coordinates()}')


if __name__ == '__main__':
    main()
