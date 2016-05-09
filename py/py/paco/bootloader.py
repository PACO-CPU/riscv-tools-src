from collections import namedtuple

CMD_NOP        =b"\x00"
CMD_SYNC       =b"\x10"
CMD_BLOCK_ADDR =b"\x21"
CMD_BLOCK_WRITE=b"\x22"
CMD_BLOCK_CRC  =b"\x23"
CMD_EXEC       =b"\x42"
CMD_LED        =b"\x51"
CMD_DIP        =b"\x52"

version_t=namedtuple("version","flags keyvalues")
default_version=version_t(set(),dict())

version_data={
  5: version_t({ "block-crc" },{ "block-size": 8 }),
  6: version_t({ "block-crc" },{ "block-size": 8 }),
  7: version_t({ "uart-shell" },{ "block-size": 32 }),
  8: version_t({ "uart-shell" },{ "block-size": 32 }),
  9: version_t({ "uart-shell" },{ "block-size": 8 }),
  10: version_t({ "uart-shell" },{ "block-size": 8 }),
}
