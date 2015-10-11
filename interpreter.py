import argparse
import sys

def interpret(program_str, step=False):
	tape = [0]
	tape_p = 0
	loopinfo_stack = [] # contains (ip, tape_p)-tuples
	def eval(cmd):
		nonlocal tape_p
		nonlocal ip

		if cmd == '>':
			if tape_p == len(tape)-1:
				# moving beyond tape, increase tape capacity
				tape.append(0)
			tape_p += 1
		elif cmd == '<':
			if tape_p == 0:
				# extend the list backwards
				tape.insert(0, 0)
			else:
				tape_p -= 1
		elif cmd == '+':
			# incr curr value
			tape[tape_p] += 1
		elif cmd == '-':
			# decr curr value
			tape[tape_p] -= 1
		elif cmd == '.':
			# prints char corresponding to value pointed at by tape_p on tape
			sys.stdout.write(chr(tape[tape_p]))
		elif cmd == ',':
			tape[tape_p] = int(input())
		elif cmd == '?':
			# prints current state
			print('idx: ' + str(tape_p) + ' tape: ' + str(tape))
		elif cmd == '[':
			if not tape[tape_p] == 0:
				# initializing a loop
				loopinfo_stack.append((ip, tape_p))
		elif cmd == ']':
			if not tape[tape_p] == 0:
				# jump back to most recent loop initialization
				ip = loopinfo_stack[len(loopinfo_stack)-1][0]
				tape_p = loopinfo_stack[len(loopinfo_stack)-1][1]
			else:
				loopinfo_stack.pop()
		else:
			print('unknown command: ' + cmd)
			sys.exit()

		if step:
			input()
			print('cmd: ' + cmd)
			print('idx: ' + str(tape_p) + ' tape: ' + str(tape))

	# strip all whitespace in input program string
	program_str = "".join(program_str.split())

	ip = 0 # instruction pointer

	if step:
		print("stepping enabled, press a key to step")
	while ip < len(program_str):
		# fetch current command
		cmd = program_str[ip]
		# evaluate
		eval(cmd)
		# increment instruction pointer
		ip += 1

def main():
    # reads input program file
	parser = argparse.ArgumentParser()
	parser.add_argument("source")
	args = parser.parse_args()

	program_file = open(args.source, 'r')
	program_str = program_file.read()
	interpret(program_str)

if __name__ == "__main__" : main()
