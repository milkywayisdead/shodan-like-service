import { isIP } from "is-ip"

const lengthGreaterThanZero = (str) => str.length > 0
const isNet = (str) => {
    const addrAndMask = str.split('/')
    if(addrAndMask.length !== 2){
        return false
    }
    const ipIsOk = isIP(addrAndMask[0])
    const mask = addrAndMask[1]
    if(mask === '') return false
    
    const mnum = Number(mask)
    const maskIsOk = !mask.includes('.') && !isNaN(mnum) && mnum >=0 && mnum <= 32
    return ipIsOk && maskIsOk
}

export default {
    hosts: isIP,
    net: isNet,
    asn: lengthGreaterThanZero,
    domain: lengthGreaterThanZero,
    port: lengthGreaterThanZero,
    country: lengthGreaterThanZero,
    city: lengthGreaterThanZero,
    org: lengthGreaterThanZero,
    soft: lengthGreaterThanZero,
    app: lengthGreaterThanZero,
    service: lengthGreaterThanZero,
    component: lengthGreaterThanZero,
    os: lengthGreaterThanZero,
}