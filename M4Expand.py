import sublime_plugin, os, subprocess
from tempfile import NamedTemporaryFile

class M4Expand(sublime_plugin.WindowCommand):
	def run(self):
		active_view = self.window.active_view()
		text = "\n\n".join(getSelectedText(active_view)).strip()

		tf = NamedTemporaryFile(mode="w", delete=False)
		try:
			tf.write(text)
			tf.close()

			res = subprocess.check_output(["m4", tf.name])
			res = res.decode('utf-8')

			panel_name = "m4expand.results"
			panel = self.window.create_output_panel(panel_name)
			self.window.run_command("show_panel", {"panel": "output." + panel_name})

			panel.set_read_only(False)
			panel.set_syntax_file(active_view.settings().get("syntax"))
			panel.run_command("append", {"characters": res})
			panel.set_read_only(True)
		except Exception as e:
			print("M4Expand - An error occurred: ", e)
		finally:
			os.unlink(tf.name)

def getSelectedText(view):
	text = []
	for s in view.sel():
		if s.empty():
			text.append(view.substr(view.line(s)))
		else:
			text.append(view.substr(s))

	return text
