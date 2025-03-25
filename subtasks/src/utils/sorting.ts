interface Orderable {
  /** Floating number that indicates the order this should be in
   * Higher values should be on the top
   */
  order: number;
}
export function getInbetweenOrder(
  index: number | undefined,
  orderableArr: Orderable[],
) {
  // If no new index or less than 2 two tasks
  if (index == undefined || orderableArr.length <= 1) return;

  let newOrder: number | undefined = undefined;

  if (index == 0) {
    newOrder = orderableArr[1].order + 0.5;
  } else if (index == orderableArr.length - 1) {
    newOrder = orderableArr[orderableArr.length - 2].order - 0.5;
  } else if (orderableArr[index + 1] && orderableArr[index - 1]) {
    newOrder =
      (orderableArr[index + 1].order + orderableArr[index - 1].order) / 2;
  }
  return newOrder;
}
