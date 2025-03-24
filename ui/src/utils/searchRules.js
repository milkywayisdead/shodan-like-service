const lengthGreaterThanZero = (str) => str.length > 0
const isIp = (str) => str.length > 0
const isNet = (str) => str.length > 0

export default {
    hosts: isIp,
    net: isNet,
    asn: lengthGreaterThanZero,
    domain: lengthGreaterThanZero,
    port: lengthGreaterThanZero,
    loc: lengthGreaterThanZero,
    org: lengthGreaterThanZero,
    soft: lengthGreaterThanZero,
    app: lengthGreaterThanZero,
    service: lengthGreaterThanZero,
    component: lengthGreaterThanZero,
    os: lengthGreaterThanZero,
}