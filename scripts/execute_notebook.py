import io
import sys
import base64
import tempfile
import os
os.environ['MPLCONFIGDIR'] = tempfile.gettempdir()

import nbformat as nbf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

notebook_path = 'spotify_tracks_eda.ipynb'
print(f"Reading {notebook_path}...")
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)

global_scope = {}
execution_count = 1

for i, cell in enumerate(nb.cells):
    if cell.cell_type == 'code':
        print(f"Executing Code Cell {execution_count} (index {i})...")
        cell.execution_count = execution_count
        cell.outputs = []
        
        # Capture stdout
        old_stdout = sys.stdout
        redirected_output = io.StringIO()
        sys.stdout = redirected_output
        
        # Close any previous plot
        plt.close('all')
        
        try:
            # We replace plt.show() with custom hook to capture figures
            executed_code = cell.source
            exec(executed_code, global_scope)
            
            # Check for printed text
            output_text = redirected_output.getvalue()
            if output_text:
                cell.outputs.append(nbf.v4.new_output(output_type='stream', name='stdout', text=output_text))
            
            # Check for open figures
            fig_nums = plt.get_fignums()
            for fnum in fig_nums:
                fig = plt.figure(fnum)
                buf = io.BytesIO()
                fig.savefig(buf, format='png', bbox_inches='tight', dpi=120)
                buf.seek(0)
                img_b64 = base64.b64encode(buf.read()).decode('utf-8')
                cell.outputs.append(nbf.v4.new_output(
                    output_type='display_data',
                    data={'image/png': img_b64, 'text/plain': '<Figure size ...>'},
                    metadata={}
                ))
            plt.close('all')
            
        except Exception as e:
            output_text = redirected_output.getvalue()
            if output_text:
                cell.outputs.append(nbf.v4.new_output(output_type='stream', name='stdout', text=output_text))
            print(f"Error in cell {execution_count}: {e}")
            cell.outputs.append(nbf.v4.new_output(
                output_type='error',
                ename=type(e).__name__,
                evalue=str(e),
                traceback=[str(e)]
            ))
        finally:
            sys.stdout = old_stdout
            
        execution_count += 1

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"All {execution_count-1} code cells executed and saved with outputs into {notebook_path}!")

