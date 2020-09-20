import unittest
from app import utils, modelHandler, decodables


class Mock2goTests(unittest.TestCase):

   # Utils

   # Compare route with the equivalent route with parameter.
    def test_utils_is_same_route(self):

        self.assertTrue(utils.is_same_route(
            'path1/route1/param', 'path1/route1/PARAMETER'))
        self.assertTrue(utils.is_same_route(
            'path1/route1/param/response', 'path1/route1/PARAMETER/response'))
        self.assertTrue(utils.is_same_route(
            'path1/route1/param1/param2', 'path1/route1/PARAMETER/PARAMETER'))
        self.assertFalse(utils.is_same_route(
            'path1/route1', 'path1/route1/PARAMETER'))

        # should be false if routes dont match number of parameters or parameter place.
        self.assertFalse(utils.is_same_route(
            'path1/route1/param1', 'path1/route1/PARAMETER/PARAMETER'))
        self.assertFalse(utils.is_same_route(
            'path1/route2/param1', 'path1/route1/PARAMETER/PARAMETER'))
        self.assertFalse(utils.is_same_route(
            'path2/route1/param1', 'path1/route1/PARAMETER/PARAMETER'))
        self.assertFalse(utils.is_same_route(
            'path1/route1', 'path1/route1/PARAMETER/PARAMETER'))
        self.assertFalse(utils.is_same_route(
            'path1', 'path1/route1/PARAMETER/PARAMETER'))
        self.assertFalse(utils.is_same_route(
            'path1/route1/param', 'path1/route1/PARAMETER/response'))
        self.assertFalse(utils.is_same_route(
            'path1/route1/response', 'path1/route1/PARAMETER/response'))

    # Find the wanted route in a list of routes without parameters.
    def test_utils_search_path_in(self):

        mock_list = ['path1/route1/response1', 'path1/route2/response1', 'path1/route2/response3',
                     'path2/route1/response2', 'path2/route2/response1', 'path3/route1/response1',
                     'path3/route1/response3', 'path4/route1/response1', 'path4/route1/response1',
                     'path4/route2/response1', 'path4/route3/response1', 'path4/route4/response4']

        self.assertIsNotNone(utils.search_path_in(
            'path1/route1/response1', mock_list))
        self.assertIsNotNone(utils.search_path_in(
            'path1/route2/response1', mock_list))
        self.assertIsNotNone(utils.search_path_in(
            'path4/route4/response4', mock_list))
        self.assertIsNotNone(utils.search_path_in(
            'path2/route2/response1', mock_list))
        self.assertIsNotNone(utils.search_path_in(
            'path3/route1/response3', mock_list))
        self.assertIsNotNone(utils.search_path_in(
            'path4/route3/response1', mock_list))

        # if route not in list, return None
        self.assertIsNone(utils.search_path_in(
            'path4/route4/response1', mock_list))
        self.assertIsNone(utils.search_path_in(
            'path1/route4/response4', mock_list))
        self.assertIsNone(utils.search_path_in(
            'path2/route3/response1', mock_list))

    # Find the wanted route in a list of routes with parameters
    def test_utils_search_path_with_param_in(self):
        mock_list = ['path1/route1/PARAMETER/PARAMETER', 'path1/PARAMETER/response1', 'path1/PARAMETER/response3/PARAMETER',
                     'path2/route1/PARAMETER', 'path2/PARAMETER/response1', 'path3/route1/PARAMETER/response1',
                     'path3/PARAMETER/response3', 'path4/PARAMETER/response1/PARAMETER', 'path4/route1/PARAMETER',
                     'path4/route2/PARAMETER', 'path4/route3/PARAMETER/response2', 'path4/route4/PARAMETER/response1']

        self.assertIsNotNone(utils.search_path_with_param_in(
            'path1/route1/param1/param2', mock_list))
        self.assertIsNotNone(utils.search_path_with_param_in(
            'path4/param1/response1/param2', mock_list))
        self.assertIsNotNone(utils.search_path_with_param_in(
            'path4/route2/param', mock_list))
        self.assertIsNotNone(utils.search_path_with_param_in(
            'path1/param1/response1', mock_list))
        self.assertIsNotNone(utils.search_path_with_param_in(
            'path4/param1/response1/param2', mock_list))
        self.assertIsNotNone(utils.search_path_with_param_in(
            'path4/route4/param/response1', mock_list))

        # if route not in list, return None
        self.assertIsNone(utils.search_path_with_param_in(
            'path4/route4/param1', mock_list))
        self.assertIsNone(utils.search_path_with_param_in(
            'path1/route4/response4', mock_list))
        self.assertIsNone(utils.search_path_with_param_in(
            'path2/route3/param1/response1', mock_list))

    # ModelHandler

    s1 = decodables.Service('service1', [decodables.Route('path1/route1', "mock1", 200, 0, []).serialize(),
                                         decodables.Route(
                                             'path1/route2', "mock2", 200, 0, []).serialize(),
                                         decodables.Route(
                                             'path1/route2/PARAMETER', "mock3", 200, 0, []).serialize(),
                                         decodables.Route('path1/route3/PARAMETER/PARAMETER', "mock4", 200, 0, []).serialize()])
    s2 = decodables.Service('service2', [decodables.Route('path2/route1', "mock5", 200, 0, []).serialize(),
                                         decodables.Route('path2/route2/PARAMETER/response1', "mock6", 200, 0, []).serialize()])
    s3 = decodables.Service('service3', [decodables.Route('path3/route1', "mock7", 200, 0, []).serialize(),
                                         decodables.Route('path3/route2/PARAMETER/PARAMETER', "mock8", 200, 0, []).serialize()])
    s4 = decodables.Service('service4', [decodables.Route('path4/route1', "mock9", 200, 0, []).serialize(),
                                         decodables.Route(
                                             'path4/PARAMETER/response1', "mock10", 200, 0, []).serialize(),
                                         decodables.Route('path4/route2', "mock11", 200, 0, []).serialize()])

    mock_services = [s1, s2, s3, s4]

    # return list of services names from list of services
    def test_modelHandler_get_services_names(self):
        self.assertEqual(modelHandler.get_services_names(self.mock_services),
                         ['service1', 'service2', 'service3', 'service4'])

    # return two lists of paths from list of services one with params another without
    def test_modelHandler_get_paths_tuple(self):
        resp = modelHandler.get_paths_tuple(self.mock_services)

        list1 = ['path1/route1', 'path1/route2', 'path2/route1',
                 'path3/route1', 'path4/route1', 'path4/route2']

        list2 = ['path1/route2/PARAMETER', 'path1/route3/PARAMETER/PARAMETER',
                 'path2/route2/PARAMETER/response1', 'path3/route2/PARAMETER/PARAMETER', 'path4/PARAMETER/response1']

        self.assertEqual(resp[0], list1)
        self.assertEqual(resp[1], list2)

    # return current reponse for path
    def test_modelHandler_get_response_from_path(self):

        # existing routes
        self.assertEqual(modelHandler.get_response_from_path(
            "path1/route1", self.mock_services), decodables.Route('path1/route1', "mock1", 200, 0, []))
        self.assertEqual(modelHandler.get_response_from_path(
            "path1/route2", self.mock_services), decodables.Route('path1/route2', "mock2", 200, 0, []))
        self.assertEqual(modelHandler.get_response_from_path(
            "path1/route3/PARAMETER/PARAMETER", self.mock_services), decodables.Route('path1/route3/PARAMETER/PARAMETER', "mock4", 200, 0, []))
        self.assertEqual(modelHandler.get_response_from_path(
            "path3/route2/PARAMETER/PARAMETER", self.mock_services), decodables.Route('path3/route2/PARAMETER/PARAMETER', "mock8", 200, 0, []))
        self.assertEqual(modelHandler.get_response_from_path(
            "path4/route1", self.mock_services), decodables.Route('path4/route1', "mock9", 200, 0, []))
        self.assertEqual(modelHandler.get_response_from_path(
            "path4/PARAMETER/response1", self.mock_services), decodables.Route('path4/PARAMETER/response1', "mock10", 200, 0, []))

        # nonexistent routes
        self.assertIsNone(modelHandler.get_response_from_path(
            "path4/PARAMETER/response2", self.mock_services))
        self.assertIsNone(modelHandler.get_response_from_path(
            "path2/PARAMETER/response2", self.mock_services))
        self.assertIsNone(modelHandler.get_response_from_path(
            "path4/PARAMETER/response4", self.mock_services))

        # path is None
        self.assertIsNone(modelHandler.get_response_from_path(
            None, self.mock_services))


if __name__ == "__main__":
    unittest.main()
