import type { ReactNode } from 'react';
import type { ApiRecord } from '../api/client.js';

type Column = {
  label: string;
  render: (record: ApiRecord) => ReactNode;
};

export default function DataTable({
  records,
  columns,
}: {
  records: ApiRecord[];
  columns: Column[];
}) {
  return (
    <div className="table-responsive">
      <table className="table table-striped table-hover align-middle">
        <thead>
          <tr>{columns.map((column) => <th scope="col" key={column.label}>{column.label}</th>)}</tr>
        </thead>
        <tbody>
          {records.map((record, index) => (
            <tr key={typeof record.id === 'string' || typeof record.id === 'number' ? record.id : index}>
              {columns.map((column) => <td key={column.label}>{column.render(record)}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
