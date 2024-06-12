### Todo List for Selenium Selectors with Additional Details

- [ ] **Manage Marketplace Settings for Porkbunai.com**

  - Selector: `#domainManagementIconButton_marketplace_porkbunai_com`
  - Additional Details:
    - `id`: domainManagementIconButton_marketplace_porkbunai_com
    - `aria-label`: manage marketplace settings for porkbunai.com
    - `data-domain-id`: 4033533
    - `data-domain`: porkbunai.com
    - `class`: btn btn-default btn-round-none domainManagementIconButton
    - `onclick`: openMarketplaceModal(this);

- [ ] **Sell Domain at Auction**

  - Selector: `#modal_marketplacePlatformSelect > div > div > div.modal-body > div:nth-child(2) > p:nth-child(4) > button`
  - Additional Details:
    - `data-domain`: porkbunai.com
    - `onclick`: $('#modal_marketplacePlatformSelect').modal('hide'); openMarketplaceModal_auction(this);
    - `style`: width:100%;
    - `class`: modal_marketplacePlatformSelect_button btn btn-porkbun-white
    - `data-domain-id`: 4033533

- [ ] **Set Auction Starting Price**

  - Selector: `#modal_userAuction_price`
  - Additional Details:
    - `aria-label`: starting price
    - `class`: form-control
    - `type`: number
    - `step`: .01
    - `name`: modal_userAuction_price
    - `id`: modal_userAuction_price
    - `autocomplete`: off

- [ ] **Set Auction End Date**

  - Selector: `#modal_userAuction_endDate`
  - Additional Details:
    - `aria-label`: end time
    - `type`: datetime-local
    - `class`: form-control
    - `name`: modal_userAuction_endDate
    - `id`: modal_userAuction_endDate
  - Desired value: `2024-06-11T14:30`
  - Code: `datetime_input.send_keys(desired_date_time)`

- [ ] **Submit Auction Form**

  - Selector: `#modal_userAuction_buttons_submit`
  - Additional Details:
    - `id`: modal_userAuction_buttons_submit
    - `class`: btn btn-primary btn-lg
    - `onclick`: setupUserAuctionDomain();

- [ ] **Enter/Submit?**
  - Ensure all fields are correctly filled and submit the form using the provided selectors.
