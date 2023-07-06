function decodeUplink(input) {
  const b = [...input.bytes];
  const len = b.length;

  if (len === 7) {
    const num = b[0];
    const tem = (b[2] << 8 | b[1]) / 100;
    const hum = (b[4] << 8 | b[3]) / 100;
    const pre = (b[6] << 8 | b[5]) / 10;
    return {
      data: { num, tem, hum, pre, len },
      warnings: [],
      errors: []
    };
  }
  if (len <= 11 && len > 7) {
    const num = b[1] << 8 | b [0];
    const tem = (b[2] << 8 | b[3]) / 100;
    const hum = (b[4] << 8 | b[5]) / 100;
    const pre = (b[6] << 8 | b[7]) / 10;
    return {
      data: { num, tem, hum, pre, len },
      warnings: [],
      errors: []
    };
  }

  return {
    data: { b, len },
    warnings: [],
    errors: []
  };
}