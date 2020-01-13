import unittest
import numpy as np
import pandas as pd

from autorank.autorank import *

pd.set_option('display.max_columns', 20)


class TestAutorank(unittest.TestCase):

    def setUp(self):
        print("In method", self._testMethodName)
        print('-------------------------------')
        self.sample_size = 50
        self.verbose = False
        np.random.seed(42)

    def tearDown(self) -> None:
        print('-------------------------------')

    # Uncomment to view created plots
#    @classmethod
#    def tearDownClass(cls):
#        plt.show()

    def test_autorank_normal_homoscedactic_two(self):
        std = 0.15
        means = [0.3, 0.7]
        data = pd.DataFrame()
        for i, mean in enumerate(means):
            data['pop_%i' % i] = np.random.normal(mean, std, self.sample_size).clip(0, 1)
        res = autorank(data, 0.05, self.verbose)
        self.assertTrue(res.all_normal)
        self.assertTrue(res.homoscedastic)
        self.assertEqual(res.omnibus, 'ttest')
        self.assertTrue(res.pvalue < res.alpha)
        plot_stats(res)
        plt.draw()
        create_report(res)
        print("----BEGIN LATEX----")
        latex_report(res, generate_plots=False)
        print("----END LATEX----")

    def test_autorank_normal_homoscedactic_two_no_difference(self):
        std = 0.15
        means = [0.3, 0.3]
        data = pd.DataFrame()
        for i, mean in enumerate(means):
            data['pop_%i' % i] = np.random.normal(mean, std, self.sample_size).clip(0, 1)
        res = autorank(data, 0.05, self.verbose)
        self.assertTrue(res.all_normal)
        self.assertTrue(res.homoscedastic)
        self.assertEqual(res.omnibus, 'ttest')
        self.assertFalse(res.pvalue<res.alpha)
        try:
            plot_stats(res)
            self.fail("ValueError expected")
        except ValueError:
            pass
        plot_stats(res, allow_insignificant=True)
        create_report(res)
        print("----BEGIN LATEX----")
        latex_report(res, generate_plots=False)
        print("----END LATEX----")

    def test_autorank_nonnormal_homoscedactic_two(self):
        std = 0.3
        means = [0.2, 0.5]
        data = pd.DataFrame()
        for i, mean in enumerate(means):
            data['pop_%i' % i] = np.random.normal(mean, std, self.sample_size).clip(0, 1)
        res = autorank(data, 0.05, self.verbose)
        self.assertFalse(res.all_normal)
        self.assertTrue(res.homoscedastic)
        self.assertEqual(res.omnibus, 'wilcoxon')
        self.assertTrue(res.pvalue<res.alpha)
        create_report(res)
        print("----BEGIN LATEX----")
        latex_report(res, generate_plots=False)
        print("----END LATEX----")

    def test_autorank_nonnormal_homoscedactic_two_no_difference(self):
        std = 0.3
        means = [0.2, 0.2]
        data = pd.DataFrame()
        for i, mean in enumerate(means):
            data['pop_%i' % i] = np.random.normal(mean, std, self.sample_size).clip(0, 1)
        res = autorank(data, 0.05, self.verbose)
        self.assertFalse(res.all_normal)
        self.assertTrue(res.homoscedastic)
        self.assertEqual(res.omnibus, 'wilcoxon')
        self.assertTrue(res.pvalue >= res.alpha)
        try:
            plot_stats(res)
            self.fail("ValueError expected")
        except ValueError:
            pass
        plot_stats(res, allow_insignificant=True)
        create_report(res)
        print("----BEGIN LATEX----")
        latex_report(res, generate_plots=False)
        print("----END LATEX----")

    def test_autorank_normal_homsocedactic(self):
        std = 0.2
        means = [0.2, 0.3, 0.5, 0.55, 0.6, 0.6, 0.9]
        data = pd.DataFrame()
        for i, mean in enumerate(means):
            data['pop_%i' % i] = np.random.normal(mean, std, self.sample_size)
        res = autorank(data, 0.05, self.verbose)
        self.assertTrue(res.all_normal)
        self.assertTrue(res.homoscedastic)
        self.assertEqual(res.omnibus, 'anova')
        self.assertEqual(res.posthoc, 'tukeyhsd')
        self.assertTrue(res.pvalue < res.alpha)
        plot_stats(res)
        plt.draw()
        create_report(res)
        print("----BEGIN LATEX----")
        latex_report(res, generate_plots=False)
        print("----END LATEX----")

    def test_autorank_normal_homsocedactic_no_difference(self):
        std = 0.2
        means = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
        data = pd.DataFrame()
        for i, mean in enumerate(means):
            data['pop_%i' % i] = np.random.normal(mean, std, self.sample_size)
        res = autorank(data, 0.05, self.verbose)
        self.assertTrue(res.all_normal)
        self.assertTrue(res.homoscedastic)
        self.assertEqual(res.omnibus, 'anova')
        self.assertEqual(res.posthoc, 'tukeyhsd')
        self.assertTrue(res.pvalue >= res.alpha)
        try:
            plot_stats(res)
            self.fail("ValueError expected")
        except ValueError:
            pass
        plot_stats(res, allow_insignificant=True)
        create_report(res)
        print("----BEGIN LATEX----")
        latex_report(res, generate_plots=False)
        print("----END LATEX----")

    def test_autorank_normal_heteroscedactic(self):
        stds = [0.05, 0.1, 0.5, 0.1, 0.05, 0.05]
        means = [0.2, 0.3, 0.5, 0.8, 0.85, 0.9]
        data = pd.DataFrame()
        for i, mean in enumerate(means):
            data['pop_%i' % i] = np.random.normal(mean, stds[i], self.sample_size)
        res = autorank(data, 0.05, self.verbose)
        self.assertTrue(res.all_normal)
        self.assertFalse(res.homoscedastic)
        self.assertEqual(res.omnibus, 'friedman')
        self.assertEqual(res.posthoc, 'nemenyi')
        self.assertTrue(res.pvalue < res.alpha)
        plot_stats(res)
        plt.draw()
        create_report(res)
        print("----BEGIN LATEX----")
        latex_report(res, generate_plots=False)
        print("----END LATEX----")

    def test_autorank_normal_heteroscedactic_no_difference(self):
        stds = [0.05, 0.1, 0.5, 0.1, 0.05, 0.05]
        means = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
        data = pd.DataFrame()
        for i, mean in enumerate(means):
            data['pop_%i' % i] = np.random.normal(mean, stds[i], self.sample_size)
        res = autorank(data, 0.05, self.verbose)
        self.assertTrue(res.all_normal)
        self.assertFalse(res.homoscedastic)
        self.assertEqual(res.omnibus, 'friedman')
        self.assertEqual(res.posthoc, 'nemenyi')
        self.assertTrue(res.pvalue >= res.alpha)
        try:
            plot_stats(res)
            self.fail("ValueError expected")
        except ValueError:
            pass
        plot_stats(res, allow_insignificant=True)
        create_report(res)
        print("----BEGIN LATEX----")
        latex_report(res, generate_plots=False)
        print("----END LATEX----")

    def test_autorank_nonnormal_homoscedactic(self):
        std = 0.3
        means = [0.2, 0.3, 0.5, 0.8, 0.85, 0.9, 0.1]
        data = pd.DataFrame()
        for i, mean in enumerate(means):
            data['pop_%i' % i] = np.random.normal(mean, std, self.sample_size).clip(0, 1)
        res = autorank(data, 0.05, self.verbose)
        self.assertFalse(res.all_normal)
        self.assertTrue(res.homoscedastic)
        self.assertEqual(res.omnibus, 'friedman')
        self.assertEqual(res.posthoc, 'nemenyi')
        self.assertTrue(res.pvalue < res.alpha)
        plot_stats(res)
        plt.draw()
        create_report(res)
        print("----BEGIN LATEX----")
        latex_report(res, generate_plots=False)
        print("----END LATEX----")

    def test_autorank_nonnormal_homoscedactic_no_difference(self):
        std = 0.3
        means = [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9]
        data = pd.DataFrame()
        for i, mean in enumerate(means):
            data['pop_%i' % i] = np.random.normal(mean, std, self.sample_size).clip(0, 1)
        res = autorank(data, 0.05, self.verbose)
        self.assertFalse(res.all_normal)
        self.assertTrue(res.homoscedastic)
        self.assertEqual(res.omnibus, 'friedman')
        self.assertEqual(res.posthoc, 'nemenyi')
        self.assertTrue(res.pvalue >= res.alpha)
        try:
            plot_stats(res)
            self.fail("ValueError expected")
        except ValueError:
            pass
        plot_stats(res, allow_insignificant=True)
        create_report(res)
        print("----BEGIN LATEX----")
        latex_report(res, generate_plots=False)
        print("----END LATEX----")

    def test_autorank_nonnormal_heteroscedactic(self):
        stds = [0.1, 0.1, 0.5, 0.1, 0.05, 0.05]
        means = [0.2, 0.3, 0.5, 0.8, 0.85, 0.9]
        data = pd.DataFrame()
        for i, mean in enumerate(means):
            data['pop_%i' % i] = np.random.normal(mean, stds[i], self.sample_size).clip(0, 1)
        res = autorank(data, 0.05, self.verbose)
        self.assertFalse(res.all_normal)
        self.assertFalse(res.homoscedastic)
        self.assertEqual(res.omnibus, 'friedman')
        self.assertEqual(res.posthoc, 'nemenyi')
        self.assertTrue(res.pvalue < res.alpha)
        plot_stats(res)
        plt.draw()
        create_report(res)
        print("----BEGIN LATEX----")
        latex_report(res, generate_plots=False)
        print("----END LATEX----")

    def test_autorank_nonnormal_heteroscedactic_no_difference(self):
        stds = [0.1, 0.1, 0.5, 0.1, 0.05, 0.05]
        means = [0.9, 0.9, 0.9, 0.9, 0.9, 0.9]
        data = pd.DataFrame()
        for i, mean in enumerate(means):
            data['pop_%i' % i] = np.random.normal(mean, stds[i], self.sample_size).clip(0, 1)
        res = autorank(data, 0.05, self.verbose)
        self.assertFalse(res.all_normal)
        self.assertFalse(res.homoscedastic)
        self.assertEqual(res.omnibus, 'friedman')
        self.assertEqual(res.posthoc, 'nemenyi')
        self.assertTrue(res.pvalue >= res.alpha)
        try:
            plot_stats(res)
            self.fail("ValueError expected")
        except ValueError:
            pass
        plot_stats(res, allow_insignificant=True)
        create_report(res)
        print("----BEGIN LATEX----")
        latex_report(res, generate_plots=False)
        print("----END LATEX----")