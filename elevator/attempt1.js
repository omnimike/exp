{
    init: (elevators, floors) => {
        this.downFloors = [];
        this.upFloors = [];
        this.elevatorDirs = [];
        for (let i = 0; i < floors.length; i++) {
            const floor = floors[i];
            floor.on('up_button_pressed', () => {
                this.upFloors[floor.floorNum()] = true;
            });
            floor.on('down_button_pressed', () => {
                this.downFloors[floor.floorNum()] = true;
            });
            this.topFloor = i;
        }
        this.bottomFloor = 0;
        for (let i = 0; i < elevators.length; i++) {
            const elevator = elevators[i];
            this.elevatorDirs[i] = 'any';
            ((elevatorNum) => {
                elevator.on('stopped_at_floor', floorNum => {
                    const dir = this.elevatorDirs[elevatorNum];
                    if (dir === 'up') {
                        this.upFloors[floorNum] = false;
                    } else if (dir === 'down') {
                        this.downFloors[floorNum] = false;
                    }
                });
            })(i);
        }
    },
    update: (dt, elevators, floors) => {
        function figureDests(i, dir) {
            const elevator = elevators[i];
            const currentFloor = floors[elevator.currentFloor()];
            let dests = elevator.getPressedFloors();
            if (dir === 'up') {
                dests = dests.concat(this.upFloors)
                    .filter(floorNum => floorNum >= currentFloor)
                    .sort();
            } else if (dir === 'down') {
                dests = dests.concat(this.downFloors)
                    .filter(floorNum => floorNum <= currentFloor)
                    .sort()
                    .reverse();
            } else if (!dests.length) {
                dests = this.upFloors.concat(this.downFloors)
                    .sort();
            }
            return dests;
        }
        function otherDir(dir) {
            return dir === 'up' ? 'down' : (dir === 'down' ? 'up' : 'any')
        }
        function figureDir(currentFloor, dests) {
            const finalFloor = dests[dests.length - 1];
            return finalFloor < currentFloor ? 'down' : (finalFloor > currentFloor ? 'up' : 'any');
        }
        function setElevatorLights(elevator, dir) {
            if (dir === 'up') {
                elevator.goingUpIndicator(true);
                elevator.goingDownIndicator(false);
            } else if (dir === 'down') {
                elevator.goingUpIndicator(false);
                elevator.goingDownIndicator(true);
            } else {
                // Strobe it up to let people feel welcomed
                elevator.goingDownIndicator(!elevator.goingDownIndicator());
                elevator.goingUpIndicator(!elevator.goingDownIndicator());
            }
        }
        
        for (let i = 0; i < elevators.length; i++) {
            const elevator = elevators[i];
            const dir = this.elevatorDirs[i];
            if (dir === 'up' || dir === 'down') {
                let dests = figureDests(i, dir);
                if (!dests.length) {
                    dests = figureDests(i, otherDir(dir));
                    if (!dests.length) {
                        dests = figureDests(i, 'any');
                    }
                }
            } else {
                dests = figureDests(i, 'any');
            }
            if (dests.length) {
                this.elevatorDirs[i] = figureDir(elevator.currentFloor(), dests);
            } else {
                this.elevatorDirs[i] = 'any';
            }
            setElevatorLights(elevator, this.elevatorDirs[i]);
            elevator.destinationQueue = dests;
            elevator.checkDestinationQueue();
        }
    }
}
