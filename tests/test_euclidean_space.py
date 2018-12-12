"""
Unit tests for the Euclidean space.
"""

import numpy as np

import geomstats.backend as gs
import geomstats.tests
import tests.helper as helper

from geomstats.euclidean_space import EuclideanSpace


class TestEuclideanSpaceMethods(geomstats.tests.TestCase):
    _multiprocess_can_split_ = True

    def setUp(self):
        gs.random.seed(1234)

        self.dimension = 2
        self.space = EuclideanSpace(self.dimension)
        self.metric = self.space.metric

        self.n_samples = 3

        self.n_points_a = gs.array([
            [2., 1.],
            [-2., -4.],
            [-5., 1.]])

    def test_random_uniform_and_belongs(self):
        point = self.space.random_uniform()
        result = self.space.belongs(point)
        expected = gs.array([[True]])

        with self.session():
            self.assertAllClose(result, expected)

    def test_squared_norm_vectorization(self):
        n_samples = self.n_samples
        n_points = self.n_points_a
        result = self.metric.squared_norm(n_points)

        expected = gs.array([[5.], [20.], [26.]])

        with self.session():
            self.assertAllClose(gs.shape(result), (n_samples, 1))
            self.assertAllClose(result, expected)

    def test_norm_vectorization(self):
        n_samples = self.n_samples
        n_points = self.n_points_a

        result = self.metric.norm(n_points)

        expected = gs.array([[2.2360679775], [4.472135955], [5.09901951359]])

        with self.session():
            self.assertAllClose(gs.shape(result), (n_samples, 1))
            self.assertAllClose(result, expected)

    @geomstats.tests.np_only
    def test_exp_vectorization(self):
        n_samples = self.n_samples
        dim = self.dimension

        one_tangent_vec = self.space.random_uniform(n_samples=1)
        one_base_point = self.space.random_uniform(n_samples=1)
        n_tangent_vecs = self.space.random_uniform(n_samples=n_samples)
        n_base_points = self.space.random_uniform(n_samples=n_samples)

        result = self.metric.exp(one_tangent_vec, one_base_point)
        expected = one_tangent_vec + one_base_point
        expected = helper.to_vector(expected)

        with self.session():
            self.assertAllClose(result, expected)

            result = self.metric.exp(n_tangent_vecs, one_base_point)
            self.assertAllClose(gs.shape(result), (n_samples, dim))

            result = self.metric.exp(one_tangent_vec, n_base_points)
            self.assertAllClose(gs.shape(result), (n_samples, dim))

            result = self.metric.exp(n_tangent_vecs, n_base_points)
            self.assertAllClose(gs.shape(result), (n_samples, dim))

    @geomstats.tests.np_only
    def test_log_vectorization(self):
        n_samples = self.n_samples
        dim = self.dimension

        one_point = self.space.random_uniform(n_samples=1)
        one_base_point = self.space.random_uniform(n_samples=1)
        n_points = self.space.random_uniform(n_samples=n_samples)
        n_base_points = self.space.random_uniform(n_samples=n_samples)

        result = self.metric.log(one_point, one_base_point)
        expected = one_point - one_base_point
        expected = helper.to_vector(expected)
        self.assertAllClose(result, expected)

        result = self.metric.log(n_points, one_base_point)
        self.assertAllClose(gs.shape(result), (n_samples, dim))

        result = self.metric.log(one_point, n_base_points)
        self.assertAllClose(gs.shape(result), (n_samples, dim))

        result = self.metric.log(n_points, n_base_points)
        self.assertAllClose(gs.shape(result), (n_samples, dim))

    @geomstats.tests.np_only
    def test_squared_dist_vectorization(self):
        n_samples = self.n_samples

        one_point_a = self.space.random_uniform(n_samples=1)
        one_point_b = self.space.random_uniform(n_samples=1)
        n_points_a = self.space.random_uniform(n_samples=n_samples)
        n_points_b = self.space.random_uniform(n_samples=n_samples)

        result = self.metric.squared_dist(one_point_a, one_point_b)
        vec = one_point_a - one_point_b
        expected = gs.dot(vec, vec.transpose())
        expected = helper.to_scalar(expected)
        self.assertAllClose(result, expected)

        result = self.metric.squared_dist(n_points_a, one_point_b)
        self.assertAllClose(gs.shape(result), (n_samples, 1))

        result = self.metric.squared_dist(one_point_a, n_points_b)
        self.assertAllClose(gs.shape(result), (n_samples, 1))

        result = self.metric.squared_dist(n_points_a, n_points_b)
        expected = gs.zeros(n_samples)
        for i in range(n_samples):
            vec = n_points_a[i] - n_points_b[i]
            expected[i] = gs.dot(vec, vec.transpose())
        expected = helper.to_scalar(expected)
        self.assertAllClose(gs.shape(result), (n_samples, 1))
        self.assertAllClose(result, expected)

    @geomstats.tests.np_only
    def test_dist_vectorization(self):
        n_samples = self.n_samples

        one_point_a = self.space.random_uniform(n_samples=1)
        one_point_b = self.space.random_uniform(n_samples=1)
        n_points_a = self.space.random_uniform(n_samples=n_samples)
        n_points_b = self.space.random_uniform(n_samples=n_samples)

        result = self.metric.dist(one_point_a, one_point_b)
        vec = one_point_a - one_point_b
        expected = gs.sqrt(gs.dot(vec, vec.transpose()))
        expected = helper.to_scalar(expected)
        self.assertAllClose(result, expected)

        result = self.metric.dist(n_points_a, one_point_b)
        self.assertAllClose(gs.shape(result), (n_samples, 1))

        result = self.metric.dist(one_point_a, n_points_b)
        self.assertAllClose(gs.shape(result), (n_samples, 1))

        result = self.metric.dist(n_points_a, n_points_b)
        expected = gs.zeros(n_samples)
        for i in range(n_samples):
            vec = n_points_a[i] - n_points_b[i]
            expected[i] = gs.sqrt(gs.dot(vec, vec.transpose()))
        expected = helper.to_scalar(expected)
        self.assertAllClose(gs.shape(result), (n_samples, 1))
        self.assertAllClose(result, expected)

    def test_belongs(self):
        point = self.space.random_uniform()
        result = self.space.belongs(point)
        expected = gs.array([[True]])

        with self.session():
            self.assertAllClose(result, expected)

    def test_random_uniform(self):
        point = self.space.random_uniform()
        point_numpy = np.random.uniform(size=(1, self.dimension))

        with self.session():
            self.assertShapeEqual(point_numpy, point)

    def test_inner_product_matrix(self):
        result = self.metric.inner_product_matrix()

        expected = gs.eye(self.dimension)
        expected = helper.to_matrix(expected)

        with self.session():
            self.assertAllClose(result, expected)

    def test_inner_product(self):
        point_a = gs.array([0., 1.])
        point_b = gs.array([2., 10.])

        result = self.metric.inner_product(point_a, point_b)
        expected = gs.dot(point_a, point_b)
        expected = helper.to_scalar(expected)

        with self.session():
            self.assertAllClose(result, expected)

    def test_inner_product_vectorization(self):
        n_samples = 3

        one_point_a = gs.array([[0., 1.]])
        one_point_b = gs.array([[2., 10.]])

        n_points_a = gs.array([
            [2., 1.],
            [-2., -4.],
            [-5., 1.]])
        n_points_b = gs.array([
            [2., 10.],
            [8., -1.],
            [-3., 6.]])

        result = self.metric.inner_product(one_point_a, one_point_b)
        expected = gs.array([[10.]])
        with self.session():
            self.assertAllClose(gs.shape(result), (1, 1))
            self.assertAllClose(result, expected)

        result = self.metric.inner_product(n_points_a, one_point_b)
        expected = gs.array([[14.], [-44.], [0.]])
        with self.session():
            self.assertAllClose(gs.shape(result), (n_samples, 1))
            self.assertAllClose(result, expected)

        result = self.metric.inner_product(one_point_a, n_points_b)
        expected = gs.array([[10.], [-1.], [6.]])
        with self.session():
            self.assertAllClose(gs.shape(result), (n_samples, 1))
            self.assertAllClose(result, expected)

        result = self.metric.inner_product(n_points_a, n_points_b)
        expected = gs.array([[14.], [-12.], [21.]])
        with self.session():
            self.assertAllClose(gs.shape(result), (n_samples, 1))
            self.assertAllClose(result, expected)

    def test_squared_norm(self):
        point = gs.array([-2., 4.])

        result = self.metric.squared_norm(point)
        expected = gs.array([[20.]])

        with self.session():
            self.assertAllClose(result, expected)

    def test_norm(self):
        point = gs.array([-2., 4.])
        result = self.metric.norm(point)
        expected = gs.array([[4.472135955]])

        with self.session():
            self.assertAllClose(result, expected)

    def test_exp(self):
        base_point = gs.array([0., 1.])
        vector = gs.array([2., 10.])

        result = self.metric.exp(tangent_vec=vector,
                                 base_point=base_point)
        expected = base_point + vector
        expected = helper.to_vector(expected)

        with self.session():
            self.assertAllClose(result, expected)

    def test_log(self):
        base_point = gs.array([0., 1.])
        point = gs.array([2., 10.])

        result = self.metric.log(point=point, base_point=base_point)
        expected = point - base_point
        expected = helper.to_vector(expected)

        with self.session():
            self.assertAllClose(result, expected)

    def test_squared_dist(self):
        point_a = gs.array([-1., 4.])
        point_b = gs.array([1., 1.])

        result = self.metric.squared_dist(point_a, point_b)
        vec = point_b - point_a
        expected = gs.dot(vec, vec)
        expected = helper.to_scalar(expected)

        with self.session():
            self.assertAllClose(result, expected)

    def test_dist(self):
        point_a = gs.array([0., 1.])
        point_b = gs.array([2., 10.])

        result = self.metric.dist(point_a, point_b)
        expected = gs.linalg.norm(point_b - point_a)
        expected = helper.to_scalar(expected)

        with self.session():
            self.assertAllClose(result, expected)

    def test_geodesic_and_belongs(self):
        n_geodesic_points = 100
        initial_point = self.space.random_uniform()
        initial_tangent_vec = gs.array([2., 0.])
        geodesic = self.metric.geodesic(
                                   initial_point=initial_point,
                                   initial_tangent_vec=initial_tangent_vec)

        t = gs.linspace(start=0., stop=1., num=n_geodesic_points)
        points = geodesic(t)

        result = self.space.belongs(points)
        expected = gs.array(n_geodesic_points * [[True]])

        with self.session():
            self.assertAllClose(expected, result)

    def test_mean(self):
        # TODO(nina): Fix the fact that it doesn't work for [1., 4.]
        point = gs.array([[1., 4.]])
        result = self.metric.mean(points=[point, point, point])
        expected = point
        expected = helper.to_vector(expected)

        with self.session():
            self.assertAllClose(result, expected)

        points = gs.array([
            [1., 2.],
            [2., 3.],
            [3., 4.],
            [4., 5.]])
        weights = gs.array([1., 2., 1., 2.])

        result = self.metric.mean(points, weights)
        expected = gs.array([16. / 6., 22. / 6.])
        expected = helper.to_vector(expected)

        with self.session():
            self.assertAllClose(result, expected)

    def test_variance(self):
        points = gs.array([
            [1., 2.],
            [2., 3.],
            [3., 4.],
            [4., 5.]])
        weights = gs.array([1., 2., 1., 2.])
        base_point = gs.zeros(2)
        result = self.metric.variance(points, weights, base_point)
        # we expect the average of the points' sq norms.
        expected = (1 * 5. + 2 * 13. + 1 * 25. + 2 * 41.) / 6.
        expected = helper.to_scalar(expected)

        with self.session():
            self.assertAllClose(result, expected)


if __name__ == '__main__':
        geomstats.test.main()
