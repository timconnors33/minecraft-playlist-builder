import { useLocation } from "react-router";
import { ReactNode, useState } from "react";
import { Pagination } from "@mui/material";

interface Props {
    children: ReactNode[];
}

function PaginatedList({ children }: Props) {

    const pageItemCount = 10;

    const [page, setPage] = useState(0);
    const pageCount = Math.ceil(children.length / pageItemCount);

    const [pageChildren, setPageChildren] = useState(children.slice(0, pageItemCount));

    const handlePageChange = (event: React.ChangeEvent<unknown>, page: number) => {
        setPage(page);
        setPageChildren(children.slice((page - 1) * pageItemCount, Math.min(page * pageItemCount + 1, children.length + 1)));
    }

    return (
        <>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
                {pageChildren}
            </div>
            {children.length > pageItemCount && (
                <Pagination sx={{ display: 'flex', justifyContent: 'center' }} count={pageCount} page={page} onChange={handlePageChange} />
            )}
        </>
    )
}

export default PaginatedList;