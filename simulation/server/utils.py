from traffic.nav import Nav

class Utils:
    @staticmethod
    def get_nav(lat1, long1, lat2, long2):
        document = [{
            "id": "document",
            "name": "Nav",
            "version": "1.0",
        }]

        fixes = Nav.get_fix_in_area(lat1, long1, lat2, long2)

        for fix in fixes:
            document.append({
                "id": fix[2],
                "position": {
                    "cartographicDegrees": [fix[1], fix[0], 0]
                },
                "point": {
                    "pixelSize": 4,
                    "color": {
                        "rgba": [39, 243, 245, 240]
                    }
                },
                "label": {
                    "text": fix[2],
                    "font": "9px sans-serif",
                    "horizontalOrigin": "LEFT",
                    "pixelOffset": {
                        "cartesian2": [10, 0],
                    },
                    # "distanceDisplayCondition": {
                    #     "distanceDisplayCondition": [0, 1000000]
                    # },
                    # "showBackground": "true",
                    # "backgroundColor": {
                    #     "rgba": [0, 0, 0, 50]
                    # }
                }
            })

        return document