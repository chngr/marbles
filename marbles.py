from datetime import date, timedelta

import os
import argparse

CLASS = "axolotl"
TITLE = ""
TEMPLATE = """\\documentclass{{{cls}}}
\\title{{{title}}}
\\author{{Raymond Cheng}}
\\date{{{today}}}
\\begin{{document}}
\\maketitle

\\end{{document}}
"""

class Log(object):
  def __init__(self, tomorrow=False):
    if tomorrow:
      self.today = (date.today() + timedelta(1)).strftime("%Y.%m.%d")
    else:
      self.today = date.today().strftime("%Y.%m.%d")
    self.header = "entry,date,compiled,sent\n"
    self.log = []
    self.current_entry = None

  def read_log(self):
    with open("Logfile", "r") as log:
      log.readline()
      for entry in log:
        entry_number, entry_date, compiled, sent = entry.split(",")
        self.log.append({ "date": entry_date
                        , "compiled": compiled == "True"
                        , "sent": sent == "True" })
    if self.today == self.log[-1]["date"]:
      self.current_entry = len(self.log) - 1
    else:
      self.current_entry = len(self.log)

  def write_log(self):
    with open("Logfile", "w") as log:
      log.write(self.header)
      for i in range(self.current_entry):
        entry = self.log[i]
        log.write("{},{},{},{}\n".format(i, entry["date"], entry["compiled"], entry["sent"]))

  def add_entry(self):
    if self.log[-1]["date"] == self.today:
      raise Exception("Stop trying to write so much today!\n")
    self.log.append({"date": log.today, "compiled": False, "sent": False})

def new_article(log):
  with open("src/{}.tex".format(log.today), "w") as f:
    f.write(TEMPLATE.format(cls=CLASS, title=TITLE, today=log.today))
  log.add_entry()

def compile_tex(log, everything=False):
  for entry in log.log:
    if not entry["compiled"] or everything:
      error = os.system("pdflatex src/{}.tex".format(entry["date"]))
      if error:
        raise Exception("Catastrophe occurred when compiling everything. Run.\n")
      entry["compiled"] = True
  os.system("rm *.out *.aux *.log *.pdfsync *.fls *.fdb_latexmk")
  os.system("mv *.pdf pdf/")

def clean():
  os.system("rm *.aux *.log *.out *.pdfsync *.fls *.fdb_latexmk pdf/*")

def clean_src():
  os.system("rm src/*.aux src/*.log src/*.out src/*.pdfsync src/*.fls src/*.pdf src/*.fdb_latexmk")

if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument("-t", "--title")
  parser.add_argument("-c", "--compile")
  parser.add_argument("-n", "--new", action="store_true")
  parser.add_argument("--clean", action="store_true")
  parser.add_argument("--tomorrow", action="store_true")
  args = parser.parse_args()
  log = Log(tomorrow=args.tomorrow)
  log.read_log()
  if args.title:
    TITLE = args.title
  if args.new:
    new_article(log)
  if args.compile:
    compile_tex(log,everything=args.compile=="all")
    clean_src()
  if args.clean:
    clean()
    clean_src()

  log.write_log()
