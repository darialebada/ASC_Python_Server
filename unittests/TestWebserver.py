import unittest
from app.task_solver import TaskSolver
from app.data_ingestor import DataIngestor
 
class TestWebserver(unittest.TestCase):
    def setUp(self):
        self.data = DataIngestor("./unittests/test_data.csv")
        self.task_solver = TaskSolver(self.data)
        self.q1 = 'Percent of adults aged 18 years and older who have an overweight classification'
        self.state1 = 'Utah'
        self.q2 = 'Percent of adults who engage in no leisure-time physical activity'
        self.state2 = 'Wyoming'
    
    def test_best5(self):
        task_res = self.task_solver.best5(self.q1)
        self.assertEqual(len(task_res), 4)
        self.assertAlmostEqual(task_res['North Dakota'], 36.6, delta=0.1)
        self.assertAlmostEqual(task_res['Utah'], 36.9, delta=0.1)
        self.assertAlmostEqual(task_res['New Mexico'], 42.9, delta=0.1)
        self.assertAlmostEqual(task_res['Arizona'], 43.6, delta=0.1)

        task_res = self.task_solver.best5(self.q2)
        self.assertEqual(len(task_res), 3)
        self.assertAlmostEqual(task_res['Kansas'], 28.7, delta=0.1)
        self.assertAlmostEqual(task_res['Wyoming'], 26.6, delta=0.1)
        self.assertAlmostEqual(task_res['Wisconsin'], 24.0, delta=0.1)

    def test_worst5(self):
        task_res = self.task_solver.worst5(self.q1)
        self.assertEqual(len(task_res), 4)
        self.assertAlmostEqual(task_res['Arizona'], 43.6, delta=0.1)
        self.assertAlmostEqual(task_res['New Mexico'], 42.9, delta=0.1)
        self.assertAlmostEqual(task_res['Utah'], 36.9, delta=0.1)
        self.assertAlmostEqual(task_res['North Dakota'], 36.6, delta=0.1)

        task_res = self.task_solver.worst5(self.q2)
        self.assertEqual(len(task_res), 3)
        self.assertAlmostEqual(task_res['Wisconsin'], 24.0, delta=0.1)
        self.assertAlmostEqual(task_res['Wyoming'], 26.6, delta=0.1)
        self.assertAlmostEqual(task_res['Kansas'], 28.7, delta=0.1)

    def test_diff_from_mean(self):
        task_res = self.task_solver.diff_from_mean(self.q1)
        self.assertEqual(len(task_res), 4)
        self.assertAlmostEqual(task_res['North Dakota'], 4.0, delta=0.1)
        self.assertAlmostEqual(task_res['New Mexico'], -2.3, delta=0.1)
        self.assertAlmostEqual(task_res['Arizona'], -3.0, delta=0.1)
        self.assertAlmostEqual(task_res['Utah'], 3.7, delta=0.1)

        task_res = self.task_solver.diff_from_mean(self.q2)
        self.assertEqual(len(task_res), 3)
        self.assertAlmostEqual(task_res['Kansas'], -2.2, delta=0.1)
        self.assertAlmostEqual(task_res['Wisconsin'], 2.5, delta=0.1)
        self.assertAlmostEqual(task_res['Wyoming'], -0.15, delta=0.1)
        
    def test_global_mean(self):
        task_res = self.task_solver.global_mean(self.q1)
        self.assertAlmostEqual(task_res["global_mean"], 40.6, delta=0.1)

        task_res = self.task_solver.global_mean(self.q2)
        self.assertAlmostEqual(task_res["global_mean"], 26.5, delta=0.1)

    def test_mean_by_category(self):
        task_res = self.task_solver.get_mean_by_category(self.q1)
        self.assertEqual(len(task_res), 5)
        self.assertAlmostEqual(task_res["('Arizona', 'Income', '$35,000 - $49,999')"], 43.6, delta=0.1)
        self.assertAlmostEqual(task_res["('New Mexico', 'Age (years)', '55 - 64')"], 40.9, delta=0.1)
        self.assertAlmostEqual(task_res["('New Mexico', 'Race/Ethnicity', 'Non-Hispanic Black')"], 45.0, delta=0.1)
        self.assertAlmostEqual(task_res["('North Dakota', 'Total', 'Total')"], 36.6, delta=0.1)
        self.assertAlmostEqual(task_res["('Utah', 'Education', 'College graduate')"], 36.9, delta=0.1)

        task_res = self.task_solver.get_mean_by_category(self.q2)
        self.assertEqual(len(task_res), 4)
        self.assertAlmostEqual(task_res["('Kansas', 'Age (years)', '45 - 54')"], 28.7, delta=0.1)
        self.assertAlmostEqual(task_res["('Wisconsin', 'Age (years)', '55 - 64')"], 24.0, delta=0.1)
        self.assertAlmostEqual(task_res["('Wyoming', 'Income', '$15,000 - $24,999')"], 29.3, delta=0.1)
        self.assertAlmostEqual(task_res["('Wyoming', 'Race/Ethnicity', 'American Indian/Alaska Native')"], 24.0, delta=0.1)

    def test_state_diff_from_mean(self):
        task_res = self.task_solver.state_diff_from_mean(self.q1, self.state1)
        self.assertAlmostEqual(task_res[self.state1], 3.7, delta=0.1)

        task_res = self.task_solver.state_diff_from_mean(self.q2, self.state2)
        self.assertAlmostEqual(task_res[self.state2], -0.15, delta=0.1)

    def test_state_mean(self):
        task_res = self.task_solver.state_mean(self.q1, self.state1)
        self.assertAlmostEqual(task_res[self.state1], 36.9, delta=0.1)

        task_res = self.task_solver.state_mean(self.q2, self.state2)
        self.assertAlmostEqual(task_res[self.state2], 26.6, delta=0.1)

    def test_states_mean(self):
        task_res = self.task_solver.states_mean(self.q1)
        self.assertEqual(len(task_res), 4)
        self.assertAlmostEqual(task_res['North Dakota'], 36.6, delta=0.1)
        self.assertAlmostEqual(task_res['Utah'], 36.9, delta=0.1)
        self.assertAlmostEqual(task_res['New Mexico'], 42.9, delta=0.1)
        self.assertAlmostEqual(task_res['Arizona'], 43.6, delta=0.1)

        task_res = self.task_solver.states_mean(self.q2)
        self.assertEqual(len(task_res), 3)
        self.assertAlmostEqual(task_res['Wisconsin'], 24.0, delta=0.1)
        self.assertAlmostEqual(task_res['Wyoming'], 26.6, delta=0.1)
        self.assertAlmostEqual(task_res['Kansas'], 28.7, delta=0.1)

    def test_state_mean_by_category(self):
        task_res = self.task_solver.state_mean_by_category(self.q1, self.state1)
        self.assertAlmostEqual(task_res['Utah']["('Education', 'College graduate')"], 36.9, delta=0.1)

        task_res = self.task_solver.state_mean_by_category(self.q2, self.state2)
        self.assertAlmostEqual(task_res['Wyoming']["('Income', '$15,000 - $24,999')"], 29.3, delta=0.1)
        self.assertAlmostEqual(task_res['Wyoming']["('Race/Ethnicity', 'American Indian/Alaska Native')"], 24.0, delta=0.1)


    

if __name__ == '__main__':
    unittest.main()
