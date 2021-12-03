def ingestListBitWords(filename):
    with open(filename) as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        #print(lines)
    return lines


def tallyBitsInReport(report):
    tally = [{} for i in range(len(report[0]))]
    for entry in report:
        for idx, val in enumerate(entry):
            if val in tally[idx]:
                tally[idx][val] += 1
            else:
                tally[idx][val] = 1
    return tally


def processReportForPower(report):
    tally = tallyBitsInReport(report)
    gamma, epsilon = "", ""
    for digitCount in tally:
        gamma += max(digitCount, key=digitCount.get)
        epsilon += min(digitCount, key=digitCount.get)
    return int(gamma, 2) * int(epsilon, 2)


def cullReportForGas(report, type):
    idx = 0
    while len(report) != 1:
        tally = tallyBitsInReport(report)
        if type == "o2":
            common = max(tally[idx], key=tally[idx].get)
        else:
            common = min(tally[idx], key=tally[idx].get)
        ##################
        #Check for multiple at same frequency
        count = 0
        for key in tally[idx]:
            if tally[idx][key] == tally[idx][common]:
                count += 1
        if count > 1:
            if type == "o2":
                common = 1
            else:
                common = 0
        ##################
        newReport = [x for x in report if x[idx] == str(common)]
        report = newReport
        idx = (idx + 1) % len(report[0])
    return newReport[0]


def processReportForGas(report):
    o2Val = cullReportForGas(report.copy(), "o2")
    co2Val = cullReportForGas(report.copy(), "co2")
    return int(o2Val, 2) * int(co2Val, 2)



###########################################

report = ingestListBitWords('inputs/3-0.1')
powerComp = processReportForPower(report)
print("Part 1 Test Input (198): " + str(powerComp))


###########################################

report = ingestListBitWords('inputs/3-1')
powerComp = processReportForPower(report)
print("Part 1 Real Input (4006064): " + str(powerComp))


###########################################

report = ingestListBitWords('inputs/3-0.1')
powerComp = processReportForGas(report)
print("Part 2 Test Input (230): " + str(powerComp))


###########################################

report = ingestListBitWords('inputs/3-1')
powerComp = processReportForGas(report)
print("Part 2 Real Input (5941884): " + str(powerComp))


###########################################

