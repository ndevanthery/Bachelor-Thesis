from pydicom import dcmread
print(12)

ds = dcmread("1-001.dcm")
print(ds)

# patient
print(ds[0x10, 0x10])
print(ds[0x10, 0x20])
