/**
 * Score points by scanning valuable fish faster than your opponent.
 **/

const FIELD_SIZE = 10000;

class Vector {
    x;
    y;
    angleGradInt;
    radiusInt;

    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.angleGradInt = this.getAngleGradInt();
        this.radiusInt = this.getRadiusInt();
    }

    toPoint() {
        return new Point(this.x, this.y);
    }

    withRotationGrad(grad) {
        const angleGrad = this.getAngleGrad();
        const newAngleGrad = angleGrad + grad;
        const newAngleRad = (newAngleGrad*Math.PI)/180;

        const radius = this.getRadius();
        const x2 = radius * Math.cos(newAngleRad);
        const y2 = radius * Math.sin(newAngleRad);

        return new Vector(Math.round(x2), Math.round(y2));
    }

    withRadius(radius) {
        const angle = this.getAngle();

        const x2 = radius * Math.cos(angle.rad);
        const y2 = radius * Math.sin(angle.rad);

        return new Vector(Math.round(x2), Math.round(y2));
    }

    withBase(x, y) {
        return new Vector(this.x + x, this.y + y);
    }

    withBaseSubtracted(x, y) {
        return new Vector(this.x - x, this.y - y);
    }

    getAngle() {
        const angleGrad = this.getAngleGrad();
        const angleRad = (angleGrad*Math.PI)/180;

        return {
            grad: angleGrad,
            rad: angleRad,
        };
    }

    getAngleGradInt() {
        return Math.round(this.getAngleGrad());
    }

    getAngleGrad() {
        return Math.round(180*Math.atan2(this.y, this.x)/Math.PI); // в градусах
    }

    getRadiusInt() {
        return Math.round(this.getRadius());
    }

    getRadius() {
        return Math.sqrt(Math.pow(this.x, 2) + Math.pow(this.y, 2));
    }

    toString() {
        return `(${this.x}, ${this.y}) ${this.angleGradInt}°`;
    }
}

class Point {
    x;
    y;

    constructor(x, y) {
        this.x = x;
        this.y = y;
    }

    toVector() {
        return new Vector(this.x, this.y);
    }

    move(vX, vY) {
        return new Point(this.x + vX, this.y + vY);
    }

    moveBy(vector) {
        return new Point(this.x + vector.x, this.y + vector.y);
    }

    fitToFrame() {
        let x = Math.max(0, this.x);
        x = Math.min(x, FIELD_SIZE);

        let y = Math.max(0, this.y);
        y = Math.min(y, FIELD_SIZE);

        return new Point(x, y);
    }

    generateMovePoints(vector, slices) {
        const result = [];

        const radius = vector.getRadius();
        for (let i = 0; i <= slices; i++) {
            let percentage = i / slices;
            let curVector = vector.withRadius(radius * percentage);
            result.push(this.moveBy(curVector));
        }

        return result;
    }

    withBaseMask(basePoint) {
        return new Point(this.x - basePoint.x, this.y - basePoint.y);
    }

    withBaseUnmask(basePoint) {
        return new Point(this.x + basePoint.x, this.y + basePoint.y);
    }

    getDistanceToPoint(point) {
        return Math.sqrt(Math.pow(point.x - this.x, 2) + Math.pow(point.y - this.y, 2));
    }

    getDistanceTo(x, y) {
        return Math.sqrt(Math.pow(x - this.x, 2) + Math.pow(y - this.y, 2));
    }

    getVerticalDistanceToPoint(point) {
        return Math.abs(point.y - this.y);
    }

    getHorizontalDistanceToPoint(point) {
        return Math.abs(point.x - this.x);
    }
}

class DirectionCalc {
    drone;
    point;
    monsters;

    constructor(drone, point, monsters) {
        this.point = point;
        this.monsters = monsters;
        this.drone = drone;
    }

    findNearestSafePath() {
        const dronePoint = new Point(this.drone.x, this.drone.y);
        const fishPoint = new Point(this.point.x, this.point.y);

        const speedVector = fishPoint.withBaseMask(dronePoint).toVector().withRadius(600);
        const pathSlicesNumber = 2;
        let curSpeedVector = null;

        /*console.error({
            drone: {
                id: this.drone.id,
                x: this.drone.x,
                y: this.drone.y,
            },
            point: this.point,
            monsters: this.monsters.map(m => {
                return {
                    x: m.x,
                    y: m.y,
                    Vx: m.Vx,
                    Vy: m.Vy,
                };
            })
        });*/

        const angleList = this.generateAngleList();
        for (let ai = 0; ai < angleList.length; ai++) {
            curSpeedVector = speedVector.withRotationGrad(angleList[ai]);
            let dronePoints = dronePoint.generateMovePoints(curSpeedVector, pathSlicesNumber);

            let validMonsters = 0;
            for (let i = 0; i < this.monsters.length; i++) {
                let isValid = true;
                let monster = this.monsters[i];
                const startMonsterPoint = new Point(monster.x, monster.y);

                let monsterPoints = startMonsterPoint.generateMovePoints(new Vector(monster.Vx, monster.Vy), pathSlicesNumber);
                for (let psi = 0; psi <= pathSlicesNumber; psi++) {

                    if (dronePoints[psi].getDistanceToPoint(monsterPoints[psi]) <= 580) {
                        isValid = false;
                        break;
                    }
                }

                let destination = dronePoint.moveBy(curSpeedVector);
                if (destination.x < 0 || destination.y < 0 || destination.x > FIELD_SIZE || destination.y > FIELD_SIZE) {
                    isValid = false;
                    break;
                }

                if (isValid) {
                    validMonsters++;
                }
            }

            if (validMonsters === this.monsters.length) {
                break;
            }
        }

        const result = dronePoint.moveBy(curSpeedVector);

        console.error({
            drone: {
                id: this.drone.id,
                x: this.drone.x,
                y: this.drone.y,
            },
            point: this.point,
            monsters: this.monsters.map(m => {
                return {
                    x: m.x,
                    y: m.y,
                    Vx: m.Vx,
                    Vy: m.Vy,
                };
            }),
            safePoint: result,
        });

        return result;
    }

    generateAngleList() {
        let angleList = Array.from({ length: 358 }, (v, k) => {
            k += 2;

            return k % 2 === 0
                ? k / 2
                : -1 * Math.floor(k / 2);
        });
        angleList = [
            0,
            ...angleList,
            180,
        ];

        return angleList;
    }
}

class Drone {
    id;
    x;
    y;
    battery;
    emergency;
    radarBlips = [];
    radarBlipsMap = {};
    unsavedScans = [];

    constructor(id, x, y, emergency, battery) {
        this.id = id;
        this.x = x;
        this.y = y;
        this.emergency = emergency;
        this.battery = battery;
    }

    getDistanceTo(point) {
        return Math.sqrt(
            Math.pow(this.x - point.x, 2)
            + Math.pow(this.y - point.y, 2)
        );
    }

    addRadarBlip(creatureId, radar) {
        this.radarBlips.push({
            creatureId,
            radar,
        });
        this.radarBlipsMap[creatureId] = radar;
    }

    addUnsavedScan(creatureId) {
        this.unsavedScans.push(creatureId);
    }

    hasUnsavedScans() {
        return this.unsavedScans.length > 0;
    }

    isEmergency() {
        return this.emergency === 1;
    }

    getPoint() {
        return new Point(this.x, this.y);
    }
    /*hasUnscannedCreaturesInRange(creatures, myScans) {
        for (let i = 0; i < creatures.length; i++) {
            let c = creatures[i];
            let found = !myScans.includes(c.id)
                && this.getDistanceTo(c) <= 800;

            if (found) {
                return true;
            }
        }

        return false;
    }*/

    isNearBorder() {
        return (this.x > 8000 && this.x < 9200)
            || (this.x > 800 && this.x < 2000)
            || (this.y > 8000 && this.y < 9200);
    }
}

class Creature {
    id;
    x;
    y;
    Vx;
    Vy;
    type;
    color;
    depthRange;

    constructor(id, x, y, Vx, Vy, type, color) {
        this.id = id;
        this.x = x;
        this.y = y;
        this.Vx = Vx;
        this.Vy = Vy;
        this.type = type;
        this.color = color;

        this.depthRange = {
            0: [2500, 5000],
            1: [5000, 7500],
            2: [7500, FIELD_SIZE],
            '-1': [2500, FIELD_SIZE],
        }[type];
    }

    toString() {
        return JSON.stringify(this);
    }

    withMove() {
        const point = new Point(this.x, this.y);
        const vector = new Vector(this.Vx, this.Vy);

        const nextPoint = point.moveBy(vector);
        const nextVector = vector.withRadius(250);
        // todo check if other drones are near

        return new Creature(this.id, nextPoint.x, nextPoint.y, nextVector.x, nextVector.y, this.type, this.color);
    }
}

/**
 *
 * @param {Drone} drone
 * @param {Number} creatureType
 * @param radarBlip
 */
function getCreatureRect(drone, creatureType, radarBlip) {
    let x1, y1, x2, y2;
    switch (radarBlip) {
        case 'TL':
            x1 = 0;
            y1 = 0;
            x2 = drone.x;
            y2 = drone.y;
            break;
        case 'TR':
            x1 = drone.x;
            y1 = 0;
            x2 = FIELD_SIZE;
            y2 = drone.y;
            break;
        case 'BL':
            x1 = 0;
            y1 = drone.y;
            x2 = drone.x;
            y2 = FIELD_SIZE;
            break;
        case 'BR':
            x1 = drone.x;
            y1 = drone.y;
            x2 = FIELD_SIZE;
            y2 = FIELD_SIZE;
            break;
        default:
            throw new Error(`Unknown radar direction ${radarBlip}`);
    }

    const depthRange = {
        0: [2500, 5000],
        1: [5000, 7500],
        2: [7500, FIELD_SIZE],
    }[creatureType];
    const saturateY = (y) => {
        if (y < depthRange[0]) {
            y = depthRange[0];
        }
        if (y > depthRange[1]) {
            y = depthRange[1];
        }

        return y;
    };

    return new Rect(x1, saturateY(y1), x2, saturateY(y2));
}

class Rect {
    x1;
    y1;
    x2;
    y2;
    constructor(x1, y1, x2, y2) {
        this.x1 = x1;
        this.y1 = y1;
        this.x2 = x2;
        this.y2 = y2;
    }

    getCenter() {
        const center = {
            x: this.x1 + Math.floor((this.x2 - this.x1) / 2),
            y: this.y1 + Math.floor((this.y2 - this.y1) / 2),
        };

        return center
    }

    getCenterPoint() {
        const center = this.getCenter();

        return new Point(center.x, center.y);
    }

    toNormalized() {
        if (this.x1 <= this.x2 && this.y1 <= this.y2) {
            return new Rect(this.x1, this.y1, this.x2, this.y2);
        }

        if (this.x2 >= this.x1 && this.y2 >= this.y1) {
            return new Rect(this.x2, this.y2, this.x1, this.y1);
        }

        throw new Error('Can not normalize rect ' + JSON.stringify(this));
    }

    /**
     * @param {Rect} other
     */
    intersection(other) {
        const a = this.toNormalized();
        const b = other.toNormalized();

        const x1 = Math.max(a.x1, b.x1);
        const y1 = Math.max(a.y1, b.y1);
        const x2 = Math.min(a.x2, b.x2);
        const y2 = Math.min(a.y2, b.y2);

        return new Rect(x1, y1, x2, y2);
    }
}

class Game {
    myDrones = [];
    myDronesMap = {};
    myScans = [];
    foeDrones = [];
    foeDronesMap = {};
    foeScans = [];
    visibleCreatures = [];
    creatureConsts = [];
    gameState;

    constructor(creatureConsts, gameState) {
        this.creatureConsts = creatureConsts;
        this.gameState = gameState;
    }

    readMyScans() {
        const myScanCount = parseInt(readline());
        for (let i = 0; i < myScanCount; i++) {
            const creatureId = parseInt(readline());

            this.myScans.push(creatureId);
        }
    }
    readFoeScans() {
        const foeScanCount = parseInt(readline());
        for (let i = 0; i < foeScanCount; i++) {
            const creatureId = parseInt(readline());

            this.foeScans.push(creatureId);
        }
    }
    readMyDrones() {
        const myDroneCount = parseInt(readline());
        for (let i = 0; i < myDroneCount; i++) {
            var inputs = readline().split(' ');
            const droneId = parseInt(inputs[0]);
            const droneX = parseInt(inputs[1]);
            const droneY = parseInt(inputs[2]);
            const emergency = parseInt(inputs[3]);
            const battery = parseInt(inputs[4]);

            let drone = new Drone(droneId, droneX, droneY, emergency, battery);
            this.myDrones.push(drone);
            this.myDronesMap[droneId] = drone;
        }
    }

    readFoeDrones() {
        const foeDroneCount = parseInt(readline());
        for (let i = 0; i < foeDroneCount; i++) {
            var inputs = readline().split(' ');
            const droneId = parseInt(inputs[0]);
            const droneX = parseInt(inputs[1]);
            const droneY = parseInt(inputs[2]);
            const emergency = parseInt(inputs[3]);
            const battery = parseInt(inputs[4]);

            const drone = new Drone(droneId, droneX, droneY, emergency, battery);
            this.foeDrones.push(drone);
            this.foeDronesMap[droneId] = drone;
        }
    }

    readDroneScans() {
        const droneScanCount = parseInt(readline());
        for (let i = 0; i < droneScanCount; i++) {
            var inputs = readline().split(' ');
            const droneId = parseInt(inputs[0]);
            const creatureId = parseInt(inputs[1]);

            const drone = this.myDronesMap[droneId] || this.foeDronesMap[droneId];
            if (drone === null) {
                continue;
            }

            /*console.error({
                droneId,
                droneScanCount,
                myDronesMap: this.myDronesMap,
            })*/

            drone.addUnsavedScan(creatureId);
        }
    }

    readCreatures() {
        const visibleCreatureCount = parseInt(readline());
        for (let i = 0; i < visibleCreatureCount; i++) {
            var inputs = readline().split(' ');
            const creatureId = parseInt(inputs[0]);
            const creatureX = parseInt(inputs[1]);
            const creatureY = parseInt(inputs[2]);
            const creatureVx = parseInt(inputs[3]);
            const creatureVy = parseInt(inputs[4]);

            const creatureConst = this.creatureConsts[creatureId];

            const creature = new Creature(creatureId, creatureX, creatureY, creatureVx, creatureVy, creatureConst.type, creatureConst.color);
            this.visibleCreatures.push(creature);

            if (creature.type === -1) {
                this.gameState.monsters[creature.id] = {
                    count: 0,
                    creature: creature,
                };
            }
        }

        let updatedMonsters = {};
        Object.entries(this.gameState.monsters).forEach(([k, v]) => {
            if (v.count === 0) {
                updatedMonsters[k] = {
                    creature: v.creature,
                    count: 1,
                };
                return;
            }

            if (v.count === 1) {
                updatedMonsters[k] = {
                    creature: v.creature.withMove(),
                    count: 2,
                };
                return;
            }
        });
        /*console.error({
            stateMonsters: this.gameState.monsters,
            updatedMonsters,
        })*/

        this.gameState.monsters = updatedMonsters;

    }

    readRadarBlips() {
        const radarBlipCount = parseInt(readline());
        for (let i = 0; i < radarBlipCount; i++) {
            var inputs = readline().split(' ');
            const droneId = parseInt(inputs[0]);
            const creatureId = parseInt(inputs[1]);
            const radar = inputs[2];

            this.myDronesMap[droneId].addRadarBlip(creatureId, radar);
        }
    }

    /**
     *
     * @param {Drone} drone
     * @returns {Creature|null}
     */
    // findNearestUnscannedVisibleCreature(drone) {
    //     let result = null;
    //     let minDistance = 999999999999;
    //     this.visibleCreatures.forEach(c => {
    //         const isScanned = this.myScans.includes(c.id) || drone.unsavedScans.includes(c.id);
    //         if (isScanned) {
    //             return;
    //         }
    //
    //         const distance = drone.getDistanceTo(c);
    //         if (distance < minDistance) {
    //             result = c;
    //             minDistance = distance;
    //         }
    //     });
    //
    //     /*console.error({
    //         droneId: drone.id,
    //         nearestUV: result,
    //         scans: this.myScans,
    //         unsavedScans: drone.unsavedScans,
    //     });*/
    //
    //     return result;
    // }

    /**
     *
     * @param {Drone} drone
     * @param {Number[]} excludeCids
     */
    listNearestUnscannedVisibleCreatures(drone, excludeCids) {
        let result = null;
        let minDistance = 999999999999;
        const list = [];

        this.visibleCreatures.forEach(c => {
            if (c.type === -1) {
                return;
            }

            if (excludeCids.includes(c)) {
                return;
            }

            const isScanned = this.myScans.includes(c.id) || this.isUnsavedScan(c.id);
            if (isScanned) {
                return;
            }

            const distance = drone.getDistanceTo(c);
            if (distance < minDistance) {
                result = c;
                minDistance = distance;
            }

            list.push({
                point: {
                    x: c.x,
                    y: c.y,
                },
                distance: distance,
                cId: c.id,
                creature: c,
            });
        });

        list.sort((a, b) => {
            if (a.distance < b.distance) {
                return -1;
            }
            if (a.distance > b.distance) {
                return 1;
            }
            return 0;
        });

        /*console.error({
            droneId: drone.id,
            nearestUV: result,
            scans: this.myScans,
            unsavedScans: drone.unsavedScans,
        });*/

        return list;
    }

    isUnsavedScan(cId) {
        for (let i = 0; i < this.myDrones.length; i++) {
            if (this.myDrones[i].unsavedScans.includes(cId)) {
                return true;
            }
        }

        return false;
    }

    getMonsters() {
        return this.visibleCreatures.filter(c => c.type === -1);
    }

    getMonstersExtended() {
        return Object.entries(this.gameState.monsters).map(([id, item]) => item.creature);
    }

    listNearestUnscannedCreatures(drone, excludeCids, game) {
        let result = null;
        let creature = null;
        let minDistance = 999999999999;
        let rect = null;
        const list = [];

        Object.entries(this.creatureConsts).forEach(([cId, {type, color}]) => {
            cId = parseInt(cId);

            if (type === -1) {
                return;
            }

            if (excludeCids.includes(cId)) {
                return;
            }

            const isScanned = this.myScans.includes(cId) || this.isUnsavedScan(cId);
            if (isScanned) {
                return;
            }

            const radarBlip = drone.radarBlipsMap[cId] || null;
            if (radarBlip === null) {
                // console.error({creatureIsGone: cId})
                return;
            }
            /*console.error({
                cId,
                type,
                color,
                blipMAp: drone.radarBlipsMap,
            })*/


            try {
                rect = getCreatureRect(drone, type, radarBlip);
                const otherDrone = game.myDrones.find(d => d.id !== drone.id);
                const otherDroneRect = getCreatureRect(otherDrone, type, otherDrone.radarBlipsMap[cId]);
                const correctedRect = rect.intersection(otherDroneRect);
                // console.error({rect, correctedRect});
                rect = correctedRect;
            } catch (e) {
                /*console.error({
                    creatureConsts: this.creatureConsts,
                    droneId: drone.id,
                    radarBlipsMap: drone.radarBlipsMap,
                });*/
                throw e;
            }

            const distance = drone.getDistanceTo(rect.getCenter());
            if (distance < minDistance) {
                result = rect.getCenter();
                creature = cId;
                minDistance = distance;
            }

            list.push({
                point: rect.getCenter(),
                distance,
                cId,
                rect,
                radarBlip,
            });
        });


        /*console.error({
            droneId: drone.id,
            cId: creature,
            center: rect?.getCenter(),
            rect: Object.assign({}, rect),
            unsavedScans: drone.unsavedScans,
        })

        console.error({
            cId: creature,
            nearestUP: result,
            blipMAp: drone.radarBlipsMap,
        });*/

        const droneSide = drone.x < 5000 ? 'left' : 'right';
        /*console.error({
            drone: drone.id,
            side: droneSide,
        })*/
        list.sort((a, b) => {
            /*const cA = this.creatureConsts[a.cId];
            const cB = this.creatureConsts[b.cId];

            const pointsMap = {
                0: 1,
                1: 2,
                2: 3,
                // '-1': 0,
            };
            const pointsA = pointsMap[cA.type];
            const pointsB = pointsMap[cB.type];

            if (pointsA < pointsB) {
                return 1;
            }

            if (pointsB < pointsA) {
                return -1;
            }*/
            /*const dronePoint = drone.point;
            const xDistA = dronePoint.getHorizontalDistanceToPoint(a.point);
            const yDistA = dronePoint.getVerticalDistanceToPoint(a.point);

            const xDistB = dronePoint.getHorizontalDistanceToPoint(b.point);
            const yDistB = dronePoint.getVerticalDistanceToPoint(b.point);*/

            let preferredBlips = {
                'left': ['BL', 'TL'],
                'right': ['BR', 'TR'],
            }[droneSide];
            const aPref = preferredBlips.includes(a.radarBlip);
            const bPref = preferredBlips.includes(b.radarBlip);

            if (aPref && !bPref) {
                return -1;
            }

            if (bPref && !aPref) {
                return 1;
            }

            const aType = this.creatureConsts[a.cId].type;
            const bType = this.creatureConsts[b.cId].type;
            // const aType3 = aType === 3;
            // const bType3 = bType === 3;
            // /**
            //  * 1: [b, a]
            //  * -1: [a, b]
            //  */
            // if (aType3 && !bType3) {
            //     return -1;
            // }
            //
            // if (bType3 && !aType3) {
            //     return 1;
            // }

            if (aType > bType) {
                return -1;
            }
            if (bType > aType) {
                return 1;
            }

            return 0;

            /*if (a.distance < b.distance) {
                return -1;
            }
            if (a.distance > b.distance) {
                return 1;
            }
            return 0;*/
        });

        return list;
    }

    init() {

    }

    toString() {
        const stringifyList = (list) => {
            return [
                '\t',
                ...list.map(obj => {
                    return obj.toString();
                })
            ].join("\n\t");
        };

        const myDrones = stringifyList(this.myDrones);
        const foeDrones = stringifyList(this.foeDrones);
        const creatures = stringifyList(this.visibleCreatures);

        return [
            `My drones: \n ${myDrones}`,
            `Foe drones: \n ${foeDrones}`,
            `Visible creatures: \n ${creatures}`,
        ].join("\n");
    }

    /*mustSave() {
        // Список можливих номінацій
        // mySaved, foeSaved, drone
        // all: mySaved + myDroneUnsaved - foeSaved
        const allCreaturesByType = Object.fromEntries();

        return false;
    }*/
}

class Radar {
    blipList = [];
    creatureRects = {};
    rectHistory = {};
    step = 0;

    constructor() {
    }
}

class Score {
    myScans;
    foeScans;
    myDrones;
    foeDrones;
    creatureTypes;

    constructor(myScans, foeScans, myDrones, foeDrones, creatureTypes) {
        this.myScans = myScans;
        this.foeScans = foeScans;
        this.myDrones = myDrones;
        this.foeDrones = foeDrones;
        this.creatureTypes = creatureTypes;
    }


}

class Combo {
    name;
    pointsDefault;
    pointsFirstToScan;
    requiredIdList;

    constructor(name, pointsDefault, pointsFirstToScan, requiredIdList) {
        this.name = name;
        this.pointsDefault = pointsDefault;
        this.pointsFirstToScan = pointsFirstToScan;
        this.requiredIdList = requiredIdList;

        this.requiredIdList.sort();
    }

    hasCompleted(saves) {
        /*const _saves = [...saves];
        _saves.sort();

        const requiredStr = this.creatureIdList.join('_');
        const savedStr = _saves.join('_');

        return requiredStr === savedStr;*/
    }

    /**
     * @param {Drone[]} drones
     * @param {Number[]} saves
     */
    check(drones, saves) {
        let rest = this.requiredIdList.filter(id => !saves.includes(id));
        if (rest.length === 0) {
            return {
                completed: true,
                collected: null,
                drones: [],
            };
        }

        const dronesWithScans = [];
        drones.forEach(d => {
            const unsavedList = rest.filter(id => d.unsavedScans.includes(id));
            if (unsavedList.length > 0) {
                dronesWithScans.push(d.id);
            }

            rest = rest.filter(id => !d.unsavedScans.includes(id));
        });

        return {
            completed: false,
            collected: rest.length === 0,
            restIds: rest,
            dronesWithScans: dronesWithScans,
        };
    }
}

class Target {
    combo;
    cost;
    saved;
    scanned;
    unsavedByDrone;
    unsaved;
    rest;

    constructor(combo, cost, saved, unsaved, unsavedByDrone) {
        this.unsavedByDrone = unsavedByDrone;
        this.combo = combo;
        this.cost = cost;

        this.saved = saved;
        this.unsaved = unsaved;
        this.scanned = [...saved, ...unsaved]
        this.rest = combo.requiredIdList.filter(id => !this.scanned.includes(id))
    }

    isComplex() {
        return this.combo.requiredIdList.length > 1;
    }

    isCompleted() {
        return this.rest.length === 0;
    }

    getDronesWithScans() {
        const result = [];
        Object.entries(this.unsavedByDrone).forEach(([dId, scans]) => {
            dId = parseInt(dId);
            if (scans.length > 0) {
                result.push(dId);
            }
        });

        return result;
    }
}

class Combos {
    /** @type {Number[]} */
    myScans;

    /** @type {Number[]} */
    foeScans;

    /** @type {Number[]} */
    creatureConsts;
    myDrones;

    /** @type {Combo[]} */
    table;

    /**
     * @returns {Target[]}
     */
    getUncompletedSortedHighestCostToLowest() {
        let sorted = [...this.table];
        sorted = sorted.filter(combo => !combo.hasCompleted(this.myScans));

        let targets = sorted.map(combo => {
            const requiredSaved = combo.requiredIdList.filter(id => this.myScans.includes(id));
            const unsaved = this.myDrones.reduce((result, drone) => {
                return [
                    ...result,
                    ...drone.unsavedScans,
                ];
            }, []);
            const requiredUnsaved = combo.requiredIdList.filter(id => unsaved.includes(id));

            const unsavedByDrone = Object.fromEntries(this.myDrones.map(drone => {
                return [
                    drone.id,
                    drone.unsavedScans.filter(id => combo.requiredIdList.includes(id))
                ];
            }));

            return new Target(
                combo,
                combo.hasCompleted(this.foeScans) ? combo.pointsDefault : combo.pointsFirstToScan,
                requiredSaved,
                requiredUnsaved,
                unsavedByDrone,
            );
        })
        targets.sort((a, b) => {
            /**
             * 1: [b, a]
             * -1: [a, b]
             */
            if (a.cost > b.cost) {
                return -1;
            }
            if (a.cost < b.cost) {
                return 1;
            }
            return 0;
        });

        return targets;
    }

    createTable() {
        const mapByType = {0: [], 1: [], 2: []};
        Object.entries(this.creatureConsts).forEach(([cId, {type, color}]) => {
            cId = parseInt(cId);
            if (type === -1) {
                return;
            }

            mapByType[type].push(cId);
        });

        const mapByColor = {0: [], 1: [], 2: [], 3: []};
        Object.entries(this.creatureConsts).forEach(([cId, {type, color}]) => {
            cId = parseInt(cId);
            if (type === -1) {
                return;
            }

            mapByColor[color].push(cId);
        });

        const table = [];
        table.push(new Combo(`All fish of one type: "0"`, 4, 8, mapByType[0]));
        table.push(new Combo(`All fish of one type: "1"`, 4, 8, mapByType[1]));
        table.push(new Combo(`All fish of one type: "2"`, 4, 8, mapByType[2]));
        table.push(new Combo(`All fish of one color : "0"`, 3, 6, mapByColor[0]));
        table.push(new Combo(`All fish of one color : "1"`, 3, 6, mapByColor[1]));
        table.push(new Combo(`All fish of one color : "2"`, 3, 6, mapByColor[2]));
        table.push(new Combo(`All fish of one color : "3"`, 3, 6, mapByColor[3]));

        Object.entries(this.creatureConsts).forEach(([cId, {type, color}]) => {
            cId = parseInt(cId);
            if (type === -1) {
                return;
            }

            const pointsMap = {
                0: 1,
                1: 2,
                2: 3,
            };
            const cost = pointsMap[type];

            table.push(new Combo(`Single fish of type ${type}`, cost, cost * 2, [cId]));
        });

        return table;
    }

    constructor(myScans, foeScans, creatureConsts, myDrones) {
        this.myDrones = myDrones;
        this.myScans = myScans;
        this.foeScans = foeScans;
        this.creatureConsts = creatureConsts;
        this.table = this.createTable();
    }
}


const gameState = {
    monsters: {}
};


const creatureCount = parseInt(readline());
const creatureConsts = {};
for (let i = 0; i < creatureCount; i++) {
    var inputs = readline().split(' ');
    const creatureId = parseInt(inputs[0]);
    const color = parseInt(inputs[1]);
    const type = parseInt(inputs[2]);
    creatureConsts[creatureId] = {color, type};
}

// game loop
while (true) {
    let game = new Game(creatureConsts, gameState);
    // console.error({creatureConsts});

    const myScore = parseInt(readline());
    const foeScore = parseInt(readline());
    // const myScanCount = parseInt(readline());
    // for (let i = 0; i < myScanCount; i++) {
    //     const creatureId = parseInt(readline());
    // }
    // const foeScanCount = parseInt(readline());
    // for (let i = 0; i < foeScanCount; i++) {
    //     const creatureId = parseInt(readline());
    // }

    game.readMyScans();
    game.readFoeScans();
    game.readMyDrones();
    game.readFoeDrones();

    // const myDroneCount = parseInt(readline());
    // for (let i = 0; i < myDroneCount; i++) {
    //     var inputs = readline().split(' ');
    //     const droneId = parseInt(inputs[0]);
    //     const droneX = parseInt(inputs[1]);
    //     const droneY = parseInt(inputs[2]);
    //     const emergency = parseInt(inputs[3]);
    //     const battery = parseInt(inputs[4]);
    // }
    // const foeDroneCount = parseInt(readline());
    // for (let i = 0; i < foeDroneCount; i++) {
    //     var inputs = readline().split(' ');
    //     const droneId = parseInt(inputs[0]);
    //     const droneX = parseInt(inputs[1]);
    //     const droneY = parseInt(inputs[2]);
    //     const emergency = parseInt(inputs[3]);
    //     const battery = parseInt(inputs[4]);
    // }

    game.readDroneScans();
    /*const droneScanCount = parseInt(readline());
    for (let i = 0; i < droneScanCount; i++) {
        var inputs = readline().split(' ');
        const droneId = parseInt(inputs[0]);
        const creatureId = parseInt(inputs[1]);
    }*/

    game.readCreatures();
    // const visibleCreatureCount = parseInt(readline());
    // for (let i = 0; i < visibleCreatureCount; i++) {
    //     var inputs = readline().split(' ');
    //     const creatureId = parseInt(inputs[0]);
    //     const creatureX = parseInt(inputs[1]);
    //     const creatureY = parseInt(inputs[2]);
    //     const creatureVx = parseInt(inputs[3]);
    //     const creatureVy = parseInt(inputs[4]);
    // }

    game.readRadarBlips();
    // const radarBlipCount = parseInt(readline());
    // for (let i = 0; i < radarBlipCount; i++) {
    //     var inputs = readline().split(' ');
    //     const droneId = parseInt(inputs[0]);
    //     const creatureId = parseInt(inputs[1]);
    //     const radar = inputs[2];
    // }

    game.init();

    // console.error(game.toString());

    const combos = new Combos(game.myScans, game.foeScans, creatureConsts, game.myDrones);
    const targetsSorted = combos.getUncompletedSortedHighestCostToLowest();
    /*console.error({targetsNumber: targetsSorted.length});
    console.error(targetsSorted);*/

    const complexCompletedTargets = targetsSorted.filter(t => t.isComplex() && t.isCompleted());
    const dronesToLift = complexCompletedTargets.length > 0
        ? complexCompletedTargets[0].getDronesWithScans()
        : [];

    let excludeCids = [];
    let prevLight = null;
    for (let i = 0; i < game.myDrones.length; i++) {
        let drone = game.myDrones[i];
        let light = '0';
        let comment = '';
        // let light = (drone.hasUnscannedCreaturesInRange(game.creatures, game.myScans) && drone.battery >= 5)
        //     ? '1'
        //     : '0';

        let list = game.listNearestUnscannedVisibleCreatures(drone, excludeCids);
        if (list.length === 0) {
            list = game.listNearestUnscannedCreatures(drone, excludeCids, game);
            // console.error({rectPoint: point});
        } else {
            // console.error({visiblePoint: point});
        }

        const monstersVisible = game.getMonsters();
        let point = null;
        if (list.length > 0) {
            excludeCids.push(list[0].cId);
            point = list[0].point;

            const distanceToPoint = drone.getPoint().getDistanceToPoint(point);
            const rect = list[0].rect;
            if (rect && distanceToPoint > 799) {
                // const radius = Math.min(distanceToPoint, 799);
                point = (new Point(drone.x, drone.y)).withBaseMask(point).toVector().withRadius(799).toPoint().withBaseUnmask(point)
            }

            let baseLightProb = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0];
            if (distanceToPoint > 800) {
                baseLightProb.push(1);
            }
            if (drone.isNearBorder() && prevLight === '0') {
                baseLightProb.push(1);
                baseLightProb.push(1);
                baseLightProb.push(1);
                baseLightProb.push(1);
                baseLightProb.push(1);
                baseLightProb.push(1);
            }
            const lightProb = baseLightProb[Math.floor(Math.random() * baseLightProb.length)];

            light = drone.y >= 3000
            && drone.battery >= 5
            && lightProb === 1
                /* && (
                     (distanceToPoint > 800 && Math.random() < 0.3 /!*&& distanceToPoint < 2000*!/)
                     || drone.y >= 6000
                 )*/
                ? '1'
                : '0';

            // comment = `going for ${list[0].cId} (${point.x}, ${point.y}), b: ${drone.battery}`;
            comment = `going for ${list[0].cId}, b: ${drone.battery}`;


            /*if (point.x < 5000) {
                point.x += 200;
                point = new Point(point.x + 200, point.y)
            } else {
                point = new Point(point.x - 200, point.y)
            }
            point = point.fitToFrame();*/
        }

        if (complexCompletedTargets.length >= 3 && dronesToLift.includes(drone.id)) {
            point = new Point(drone.x, 500);
            light = '0';
        }

        /*if (
            (drone.hasUnsavedScans() && drone.unsavedScans.length % 5 === 0)
            || point === null
        ) {
            // console.log(`MOVE ${drone.x} 500 0`);
            // continue;
            point = new Point(drone.x, 500);
        }*/

        /*if (game.mustSave()) {
            point = new Point(drone.x, 500);
        }*/

        if (point === null) {
            point = new Point(drone.x, 500);
            light = '0';
        }


        const monsters = game.getMonstersExtended();
        /*console.error({
            monstersVisible,
            monstersExtended: monsters,
        });*/
        if (point) {
            let calc = new DirectionCalc(drone, point, monsters);
            point = calc.findNearestSafePath().fitToFrame();
        }

        if (drone.isEmergency()) {
            comment = 'emergency';
        }

        prevLight = light;

        let command = point
            ? `MOVE ${point.x} ${point.y} ${light} ${comment}`
            : `WAIT ${light} ${comment}`

        // Write an action using console.log()
        // To debug: console.error('Debug messages...');

        console.log(command);         // MOVE <x> <y> <light (1|0)> | WAIT <light (1|0)>

    }
}
