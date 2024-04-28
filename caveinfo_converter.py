class Scanner:
    def __init__(self, text: str):
        self.tokens = text.split()
        self.index = 0
    def skip_after_symbol(self, symbol: str) -> str:
        if self.next() == symbol:
            return symbol
        else:
            self.skip_after_symbol(symbol)
    def next_int(self) -> int:
        return int(self.next())
    def next_float(self) -> float:
        return float(self.next())
    def current(self) -> str:
        return self.tokens[self.index]
    def next(self) -> str:
        value = self.tokens[self.index]
        self.index += 1
        return value

class CaveInfoConverter:
    def __init__(self):
        self.tokens = []
    def to_dict(self, caveinfo_text: str) -> dict:
        text = self.remove_hash_comment(caveinfo_text)
        scanner = Scanner(text)
        output_data = {}
        scanner.skip_after_symbol('}')
        output_data['numSublevels'] = scanner.next_int()
        output_data['floors'] = []

        for sublevel in range(output_data['numSublevels']):
        
            floor = {}
            scanner.skip_after_symbol('{')

            floorInfo = {}
            while True:
                id = scanner.next()
                if id == '{_eof}':
                    break
                inter = scanner.next()
                match id:
                    case '{f000}' | '{f001}':
                        floorInfo['sublevel'] = scanner.next_int()
                    case '{f002}':
                        floorInfo['maxMainTeki'] = scanner.next_int()
                    case '{f003}':
                        floorInfo['maxItem'] = scanner.next_int()
                    case '{f004}':
                        floorInfo['maxGate'] = scanner.next_int()
                    case '{f014}':
                        floorInfo['capProb'] = scanner.next_int() / 100
                    case '{f005}':
                        floorInfo['maxRoom'] = scanner.next_int()
                    case '{f006}':
                        floorInfo['corridorProb'] = scanner.next_float()
                    case '{f007}':
                        floorInfo['hasGeyser'] = scanner.next_int() == 1
                    case '{f008}':
                        floorInfo['caveUnitFile'] = scanner.next()
                    case '{f009}':
                        floorInfo['lightingFile'] = scanner.next()
                    case '{f00A}':
                        floorInfo['skyboxFile'] = scanner.next()
                    case '{f010}':
                        floorInfo['holeClogged'] = scanner.next_int() == 1
                    case '{f011}':
                        floorInfo['echoStrength'] = scanner.next_int()
                    case '{f012}':
                        floorInfo['musicType'] = scanner.next_int()
                    case '{f013}':
                        floorInfo['hasFloorPlane'] = scanner.next_int() == 1
                    case '{f015}':
                        floorInfo['allowCapSpawns'] = scanner.next_int() == 1
                    case '{f016}':
                        floorInfo['waterwraithTimer'] = scanner.next_float()
                    case '{f017}':
                        floorInfo['hasSeesaw'] = scanner.next_int() != 0
                    case _:
                        pass
            floor['floorInfo'] = floorInfo
            
            tekiInfo = []
            scanner.skip_after_symbol('{')
            n = scanner.next_int()
            for i in range(n):
                teki = {
                    'rawTekiName': scanner.next(),
                    'rawWeight': scanner.next_int(),
                    'type': scanner.next_int(),
                }
                tekiInfo.append(teki)
            floor['tekiInfo'] = tekiInfo

            itemInfo = []
            scanner.skip_after_symbol('{')
            n = scanner.next_int()
            for i in range(n):
                item = {
                    'itemName': scanner.next(),
                    'rawWeight': scanner.next_int(),
                }
                itemInfo.append(item)
            floor['itemInfo'] = itemInfo

            gateInfo = []
            scanner.skip_after_symbol('{')
            n = scanner.next_int()
            for i in range(n):
                gate = {
                    'gateName': scanner.next(),
                    'gateLife': scanner.next_float(),
                    'weight': scanner.next_int(),
                }
                gateInfo.append(gate)
            floor['gateInfo'] = gateInfo

            capInfo = []
            scanner.skip_after_symbol('{')
            n = scanner.next_int()
            for i in range(n):
                cap = {
                    'capType': scanner.next_int(),
                    'rawTekiName': scanner.next(),
                    'rawWeight': scanner.next_int(),
                    'type': scanner.next_int(),
                }
                capInfo.append(cap)
            floor['capInfo'] = capInfo

            output_data['floors'].append(floor)

        return output_data

    @staticmethod
    def remove_hash_comment(text: str) -> str:
        lines = [line.split('#')[0].strip() for line in text.splitlines()]
        lines = [line for line in lines if len(line) > 0]
        return '\n'.join(lines)

if __name__ == '__main__':

    import yaml
    from pathlib import Path
    CAVEINFO_FILE_DIR = Path(__file__).parent / 'files'
    YAML_FILE_DIR = Path(__file__).parent / 'yaml-output'
    reader = CaveInfoConverter()

    metainfo = yaml.safe_load(open(CAVEINFO_FILE_DIR / 'metainfo.yaml'))
    cave_all: list[str] = metainfo['cave']['all']

    for caveinfo_file_path in CAVEINFO_FILE_DIR.glob('**/*.txt'):
        output_dict = reader.to_dict(open(caveinfo_file_path).read())
        output_yaml = yaml.dump(output_dict, sort_keys=False)
        output_path = (YAML_FILE_DIR / caveinfo_file_path.relative_to(CAVEINFO_FILE_DIR)).with_suffix('.yaml')
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(output_yaml)
