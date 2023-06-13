import hl7
hl7_message = '''MSH|^~\\&|HIS|LAB|HOSP|RAD|202201011200||ORU^R01|1|P|2.5\r
PID|1||123456789|Doe^John||19800101|M\r
OBR|1|1234|US-1234^Abdominal ultrasound^L|||202201011200|||John Doe|||202201011300|||||||F|||202201011300\r
OBX|1|CE|1111^Report Status^L||F|||R|||202201011300\r
OBX|2|TX|2222^Report^L||Patient has a normal appearing liver and gallbladder. No evidence of gallstones or biliary obstruction.|||R|||202201011300\r
'''
# Parse the HL7 message
parsed_message = hl7.parse(hl7_message)

print(len(parsed_message))
# Access the individual segments of the message
msh_segment = parsed_message[0]
pid_segment = parsed_message[1]

for info in pid_segment:
    print(info)