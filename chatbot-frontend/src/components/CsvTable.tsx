import React from "react";
import { Table, Thead, Tbody, Tr, Th, Td, Box } from "@chakra-ui/react";

export interface DataItem {
  [key: string]: any;
}

export interface CSVTableProps {
  data: DataItem[];
}

const CSVTable: React.FC<CSVTableProps> = ({ data }) => {
  return (
    <Box bg="white" p={4} borderRadius="md" shadow="md" marginBottom="10px">
      <Table variant="simple">
        <Thead>
          <Tr>
            {data.length > 0 &&
              Object.keys(data[0]).map((key) => <Th key={key}>{key}</Th>)}
          </Tr>
        </Thead>
        <Tbody>
          {data.map((row, index) => (
            <Tr key={index}>
              {Object.keys(row).map((key) => (
                <Td key={key} textAlign="center" textColor="black">
                  {row[key]}
                </Td>
              ))}
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Box>
  );
};

export default CSVTable;
