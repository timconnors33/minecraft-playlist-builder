import { useLocation } from "react-router";
import { ReactNode, useEffect, useState } from "react";
import { Pagination, Paper } from "@mui/material";

interface Props {
    children: ReactNode[];
}

function PaginatedList({ children }: Props) {

    const pageItemCount = 10;

    const [page, setPage] = useState(1);
    const pageCount = Math.ceil(children.length / pageItemCount);

    const [pageChildren, setPageChildren] = useState(children.slice(0, pageItemCount));

    useEffect(() => {
        setPageChildren(children.slice((page - 1) * pageItemCount, Math.min(page * pageItemCount, children.length)));
    }, [children])

    const handlePageChange = (event: React.ChangeEvent<unknown>, page: number) => {
        setPage(page);
        setPageChildren(children.slice((page - 1) * pageItemCount, Math.min(page * pageItemCount, children.length)));
    }

    return (
        <div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginTop: '10px', marginBottom: '10px'}}>
                {pageChildren}
            </div>
            {children.length > pageItemCount && (
                <Pagination sx={{ display: 'flex', justifyContent: 'center'}} count={pageCount} page={page} onChange={handlePageChange} />
            )}
        </div>
    )
}

export default PaginatedList;