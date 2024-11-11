import { createSlice } from "@reduxjs/toolkit";
import { fetchItem, fetchItems, fetchOrderBills, fetchSuppliers, fetchInventories, fetchRequisitions, fetchPurchaseOrders, fetchIncomingItems } from "@/redux/service/inventory";


const initialState = {
  inventories: [],
  inventoryItems: [],
  requisitions: [],
  purchaseOrderItems: [],
  purchaseOrders: [],
  items: [],
  suppliers: [],
  orderBills: [],
  item: [],
  incomingItems: [],
};

const InventorySlice = createSlice({
  name: "inventory",
  initialState,
  reducers: {
    setItems: (state, action) => {
      state.items = action.payload;
    },
    setSuppliers: (state, action) => {
      state.suppliers = action.payload;
    },
    setOrderBills: (state, action) => {
      state.orderBills = action.payload;
    },
    setItem: (state, action) => {
      state.item = action.payload;
    },
    updateItem: (state, action) => {
      // Find the index of the item with the same id as action.payload.id
      const index = state.item.findIndex(item => parseInt(item.id) === parseInt(action.payload.id));
      
      if (index !== -1) {
        // Update the item at the found index with the new data from action.payload
        state.item[index] = {
          ...state.item[index], // Keep existing properties
          ...action.payload       // Override with new data
        };
      }
    },
    setInventories: (state, action) => {
      state.inventories = action.payload;
    },
    setRequisitions: (state, action) => {
      state.requisitions = action.payload;
    },
    setPurchaseOrders: (state, action) => {
      state.purchaseOrders = action.payload;
    },
    setIncoming:(state, action) => {
      state.incomingItems = action.payload;
    },
    clearInventoryItemsPdf: (state, action)=>{
      state.inventoryItems = [];
    },
    setInventoryItemsPdf: (state, action) => {
      const inventoryItem = state.inventoryItems.filter(item => item.item != action.payload.item );
      state.inventoryItems = inventoryItem;
    },
    setInventoryItems: (state, action) => {

      const inventoryItem = state.inventoryItems.find(item => item.item === action.payload.item );
      if (inventoryItem) {
        // If inventoryItem is found, update the existing item in the array
        state.inventoryItems = state.inventoryItems.map(item =>
          item.item === action.payload.item ? { ...item, date_created:action.payload.date_created, supplier:action.payload.supplier, quantity_requested:action.payload.quantity_requested } : item
        );
      } else {
        // If inventoryItem is not found, add the new item to the array
        state.inventoryItems = [...state.inventoryItems, action.payload];
      }
    },

    clearPurchaseOrderItemsPdf: (state, action)=>{
      state.purchaseOrderItems = [];
    },
    setPurchaseOrderItemsPdf: (state, action) => {
      const purchaseOrderItem = state.purchaseOrderItems.filter(item => item.item != action.payload.item );
      state.purchaseOrderItems = purchaseOrderItem;
    },
    setPurchaseOrderItems: (state, action) => {

      const purchaseOrderItem = state.purchaseOrderItems.find(item => item.item === action.payload.item );
      if (purchaseOrderItem) {
        // If PurchaseOrderItem is found, update the existing item in the array
        state.purchaseOrderItems = state.purchaseOrderItems.map(item =>
          item.item === action.payload.item ? { ...item, date_created:action.payload.date_created, supplier:action.payload.supplier, quantity_purchased:action.payload.quantity_purchased } : item
        );
      } else {
        // If PurchaseOrderItem is not found, add the new item to the array
        state.purchaseOrderItems = [...state.purchaseOrderItems, action.payload];
      }
    },
  },
});

export const { updateItem, setItems,setSuppliers,setOrderBills,setItem, setInventories, setRequisitions, setPurchaseOrders, setInventoryItems, setInventoryItemsPdf, clearInventoryItemsPdf, setPurchaseOrderItems, setPurchaseOrderItemsPdf, clearPurchaseOrderItemsPdf, setIncoming } = InventorySlice.actions;


export const getAllItems = () => async (dispatch) => {
  try {
    const response = await fetchItems();
    dispatch(setItems(response));
  } catch (error) {
    console.log("ITEMS_ERROR ", error);
  }
};

export const getAllInventories = (auth) => async (dispatch) => {
  try {
    const response = await fetchInventories(auth);
    dispatch(setInventories(response));
  } catch (error) {
    console.log("INVENTORIES_ERROR ", error);
  }
};

export const getAllRequisitions = (auth) => async (dispatch) => {
  try {
    const response = await fetchRequisitions(auth);
    dispatch(setRequisitions(response));
  } catch (error) {
    console.log("REQUISITIONS_ERROR ", error);
  }
};

export const getAllPurchaseOrders = (auth) => async (dispatch) => {
  try {
    const response = await fetchPurchaseOrders(auth);
    dispatch(setPurchaseOrders(response));
  } catch (error) {
    console.log("PURCHASE_ORDERS_ERROR ", error);
  }
};

export const getAllIncomingItems = (auth) => async (dispatch) => {
  try {
    const response = await fetchIncomingItems(auth);
    dispatch(setIncoming(response));
  } catch (error) {
    console.log("PURCHASE_ORDERS_ERROR ", error);
  }
};

export const getItems = () => async (dispatch) => {
  try {
    const response = await fetchItem();
    dispatch(setItem(response));
  } catch (error) {
    console.log("ITEMS_ERROR ", error);
  }
};

export const getAllSuppliers = () => async (dispatch) => {
  try {
    const response = await fetchSuppliers();
    dispatch(setSuppliers(response));
  } catch (error) {
    console.log("SUPPLIERS_ERROR ", error);
  }
};

export const getAllOrderBills = () => async (dispatch) => {
  try {
    const response = await fetchOrderBills();
    dispatch(setOrderBills(response));
  } catch (error) {
    console.log("SUPPLIERS_ERROR ", error);
  }
};

export const addItemToInventoryPdf = (payload) => (dispatch) => {
  dispatch(setInventoryItems(payload));
};

export const removeItemToInventoryPdf = (payload) => (dispatch) => {
  dispatch(setInventoryItemsPdf(payload));
};

export const clearItemsToInventoryPdf = () => (dispatch) => {
  dispatch(clearInventoryItemsPdf());
};

export const addItemToPurchaseOrderPdf = (payload) => (dispatch) => {
  dispatch(setPurchaseOrderItems(payload));
};

export const removeItemToPurchaseOrderPdf = (payload) => (dispatch) => {
  dispatch(setPurchaseOrderItemsPdf(payload));
};

export const clearItemsToPurchaseOrderPdf = () => (dispatch) => {
  dispatch(clearPurchaseOrderItemsPdf());
};

export const updateAnItem = (item) => (dispatch) => {
  dispatch(updateItem(item));
};


export default InventorySlice.reducer;
