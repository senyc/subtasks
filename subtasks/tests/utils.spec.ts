import { getInbetweenOrder } from "../src/utils/sorting";
import { beforeEach, describe, expect, it } from "vitest";

interface Orderable {
  order: number;
}
describe("getInbetweenOrder", () => {
  let orderableArr: Orderable[];

  beforeEach(() => {
    orderableArr = [{ order: 10 }, { order: 20 }, { order: 30 }, { order: 40 }];
  });

  it("should return undefined when no index is provided", () => {
    expect(getInbetweenOrder(undefined, [])).toBeUndefined();
    expect(getInbetweenOrder(undefined, [orderableArr[0]])).toBeUndefined();
  });

  describe("when index is valid", () => {
    it("should calculate order for first position", () => {
      expect(getInbetweenOrder(0, orderableArr)).toEqual(
        orderableArr[1].order + 0.5,
      );
    });

    it("should calculate order for last position", () => {
      expect(getInbetweenOrder(orderableArr.length - 1, orderableArr)).toEqual(
        orderableArr[orderableArr.length - 2].order - 0.5,
      );
    });

    it("should calculate average of neighbors when in middle", () => {
      const index = 2;
      expect(getInbetweenOrder(index, orderableArr)).toEqual((20 + 40) / 2);
    });
  });
});
