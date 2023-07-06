function decodeUplink(input) {
  function toInt16(int16){
    if (int16 & 0x8000) {
      int16 = -(0x10000 - int16);
    }
    return int16;
  }
  const b = [...input.bytes];
  const len = b.length;

  if (len === 7) {
    const num = b[0];
    const rol = toInt16(b[2] << 8 | b[1]) / 100;
    const pit = toInt16(b[4] << 8 | b[3]) / 100;
    const acc = toInt16(b[6] << 8 | b[5]) / 100;
    const flag = false;
    return {
      data: { num, acc, rol, pit, flag, len },
      warnings: [],
      errors: []
    };
  }
  if (len <= 11 && len > 7) {
    const num = b[1] << 8 | b [0];
    var flag = toInt16(b[6] << 8 | b[7]);
    if (flag ===2){
      const lat = toInt16(b[2] << 8 | b[3]);
      const lon = toInt16(b[4] << 8 | b[5]);
      flag = true;
      return {
      data: { num, lat, lon, flag, len },
      warnings: [],
      errors: []
    };
    }else{
      const rol = toInt16(b[2] << 8 | b[3]) / 100;
      const pit = toInt16(b[4] << 8 | b[5]) / 100;
      const acc = flag/100;
      flag = false;
      return {
      data: { num, acc, rol, pit, flag, len },
      warnings: [],
      errors: []
    };
    }
  }

  return {
    data: { b, len },
    warnings: [],
    errors: []
  };
}