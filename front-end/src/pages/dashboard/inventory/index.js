import React, { useState } from "react";
import { Link } from 'react-router-dom'
import { Container, Grid } from "@mui/material";
import InventoryDataGrid from "@/components/dashboard/inventory";
import AuthGuard from "@/assets/hoc/auth-guard";
import CustomizedLayout from "@/components/layout/customized-layout";
import IncomingItems from "@/components/dashboard/inventory/incoming-items";
import Reports from "@/components/dashboard/inventory/reports";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AddInventory from "@/components/dashboard/inventory/AddInventory";

const Inventory = () => {
  const [currentTab, setCurrentTab] = useState(0);

  return (

    <Router>
      <div>
      <Container maxWidth="xl">
        <div className="flex items-center gap-4 my-8">
          <Link to='/dashboard/inventory' onClick={()=> setCurrentTab(0)} className={`${currentTab === 0 ? 'bg-primary text-white' : 'bg-white shadow'}  text-sm rounded px-3 py-2 mb-1`}>
            Inventory
          </Link>
          <Link to='/dashboard/inventory' onClick={()=> setCurrentTab(1)} className={`${currentTab === 1 ? 'bg-primary text-white' : 'bg-white shadow'}  text-sm rounded px-3 py-2 mb-1`}>
            Purchase Order
          </Link>
          <Link to='/dashboard/inventory' onClick={()=> setCurrentTab(2)} className={`${currentTab === 2 ? 'bg-primary text-white' : 'bg-white shadow'}  text-sm rounded px-3 py-2 mb-1`}>
            Requisition Entry
          </Link>
          {/* <RequisitionModal /> */}
          <Link to='/dashboard/inventory/incoming-items' onClick={()=> setCurrentTab(3)} className={`${currentTab === 3 ? 'bg-primary text-white' : 'bg-white shadow'}  text-sm rounded px-3 py-2 mb-1`}>
            Incoming Items
          </Link>
          <Link to='/dashboard/inventory/report' onClick={()=> setCurrentTab(4)} className={`${currentTab === 4 ? 'bg-primary text-white' : 'bg-white shadow'}  text-sm rounded px-3 py-2 mb-1`}>
            Reports
          </Link>
        </div>

        <Routes>
          <Route path="/dashboard/inventory" exact element={<InventoryDataGrid />} />
          <Route path="/dashboard/inventory/add-inventory" exact element={<AddInventory />} />
          <Route path="/dashboard/inventory/incoming-items" exact element={<IncomingItems />} />
          <Route path="/dashboard/inventory/report" exact element={<Reports />} />

          {/* <Route path="/about" component={About} /> */}
        </Routes>
      </Container>
        
      </div>
    </Router>

  );
};

Inventory.getLayout = (page) => (
  <AuthGuard>
    <CustomizedLayout>{page}</CustomizedLayout>;
  </AuthGuard>
);

export default Inventory;
