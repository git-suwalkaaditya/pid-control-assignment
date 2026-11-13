
import runpy

for script in ["sec1_loop_diagram.py", "sec4_metrics.py", "sec5_each_part.py",
               "sec6_compare.py", "sec7_real_world.py", "sec8_ziegler_nichols.py",
               "sec9_final_controller.py", "report_figures.py"]:
    print(f"\n===== {script} =====")
    runpy.run_path(script, run_name="__main__")
