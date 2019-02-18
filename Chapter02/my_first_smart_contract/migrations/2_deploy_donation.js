var Donation = artifacts.require("./Donation.sol");

module.exports = function(deployer) {
  deployer.deploy(Donation);
};
