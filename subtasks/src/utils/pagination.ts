export function calculateOffsetLimit({
  page,
  pageSize,
}: {
  /** This value is expected to be one indexed*/
  page: number;
  pageSize: number;
}) {
  const offset = (page - 1) * pageSize;
  const limit = page * pageSize;
  /** These values are expected to be 0-indexed as they are used in the query*/
  return [offset, limit];
}
