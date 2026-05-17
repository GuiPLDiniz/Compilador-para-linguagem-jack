from vm_writer import VMWriter

writer = VMWriter()

writer.write_push("constant", 10)
writer.write_pop("local", 0)
writer.write_arithmetic("add")
writer.write_call("Math.multiply", 2)

print(writer.get_output())