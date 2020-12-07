class Map:

    def configure(self, data):
        self.indexMap = data['result']['indexMap']
        self.intersectionCoordinates = data['result']['intersectionCoordinates']
        self.map = data['result']['map']
        self.playerID = data['playerID']
        if not data['success']:
            print('Map reading failed.')

    def get_neighbours(self, position):
        return self.indexMap[position]

    def get_resources(self, cities):
        resources = {'water': 0, 'dust': 0, 'sheep': 0, 'wood': 0, 'wheat': 0, 'clay': 0, 'iron': 0}
        for city in cities:
            resource_coordinates = self.intersectionCoordinates[city[0]]
            for coordinate in resource_coordinates:
                for resource in self.map['tiles']:
                    for r in resource:
                        if r is not None and r['coordinates']['x'] == coordinate['x'] \
                                and r['coordinates']['y'] == coordinate['y']:
                            if city[1] == 1:
                                resources[r['resourceType'].lower()] += r['resourceWeight']
                            else:
                                resources[r['resourceType'].lower()] += 2*r['resourceWeight']
        return resources

    def is_water(self, start, end):
        coordinates1 = self.intersectionCoordinates[start]
        coordinates2 = self.intersectionCoordinates[end]

        water_type1 = 0
        water_type2 = 0

        for coordinate in coordinates1:
            row = self.map['tiles'][int(coordinate['x'])]
            resource = row[int(coordinate['y'])]
            if resource is not None:
                if resource['resourceType'] == 'WATER':
                    water_type1 += 1

        for coordinate in coordinates2:
            row = self.map['tiles'][int(coordinate['x'])]
            resource = row[int(coordinate['y'])]
            if resource is not None:
                if resource['resourceType'] == 'WATER':
                    water_type2 += 1

        if water_type1 >= 2 and water_type2 >= 2:
            return True

        return False
